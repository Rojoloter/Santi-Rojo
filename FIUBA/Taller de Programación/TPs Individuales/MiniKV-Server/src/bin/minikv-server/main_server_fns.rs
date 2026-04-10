use crate::minikv_server::Minikv;
use minikv::errors::KvError;
use minikv::errors::{format_error, print_error};
use std::env;
use std::fs::{File, OpenOptions};
use std::io::{BufRead, BufReader, Write};
use std::net::{TcpListener, TcpStream};
use std::path::Path;
use std::sync::{Arc, RwLock};

/// Valida los archivos y carga los datos en memoria
pub fn initialize_storage(log_path: &str, data_path: &str) -> Option<Arc<RwLock<Minikv>>> {
    if !Path::new(log_path).exists() || !Path::new(data_path).exists() {
        create_or_truncate_file(log_path.to_string(), data_path.to_string());
    }
    let mut storage = Minikv::new();
    if storage
        .load_from_file(data_path.to_string(), false)
        .is_err()
    {
        print_error(KvError::InvalidDataFile);
        return None;
    }
    if storage.load_from_file(log_path.to_string(), true).is_err() {
        print_error(KvError::InvalidLogFile);
        return None;
    }

    Some(Arc::new(RwLock::new(storage)))
}

/// Lee los argumentos de la consola y bindea el puerto
pub fn initialize_listener() -> Option<TcpListener> {
    let args: Vec<String> = env::args().collect();
    let Some(addr) = args.get(1) else {
        print_error(KvError::InvalidArgs);
        return None;
    };
    match TcpListener::bind(addr.as_str()) {
        Ok(l) => Some(l),
        Err(_) => {
            print_error(KvError::ServerSocketBinding);
            None
        }
    }
}

/// Maneja cada cliente conectado en un hilo distinto
pub fn handle_client(
    stream: TcpStream, // Le sacamos el 'mut' a la firma
    storage: Arc<RwLock<Minikv>>,
    log_path: &str,
    data_path: &str,
) {
    let mut reader = BufReader::new(stream);
    let mut line = String::new();
    loop {
        line.clear();
        match reader.read_line(&mut line) {
            Ok(0) | Err(_) => {
                print_error(KvError::ConnectionClosed);
                break;
            }
            Ok(_) => {}
        }
        if line.trim().is_empty() {
            continue;
        }
        let parts = Minikv::split_words(line.trim_end().to_string());
        let response = process_command(log_path, data_path, &parts, &storage);
        if writeln!(reader.get_mut(), "{}", response).is_err() {
            print_error(KvError::ConnectionClosed);
            break;
        }
    }
}

/// Crea o limpia un archivo a partir de un path
pub fn create_or_truncate_file(log_path: String, data_path: String) {
    if File::create(log_path).is_err() {
        print_error(KvError::InvalidLogFile)
    };
    if File::create(data_path).is_err() {
        print_error(KvError::InvalidDataFile)
    };
}

/// Escribe la clave - valor en el log y actualiza el HashMap
fn handle_set(log_path: &str, parts: &[String], storage: &mut Minikv) -> String {
    let Ok(mut file) = OpenOptions::new().append(true).open(log_path) else {
        return format_error(KvError::InvalidLogFile);
    };
    if parts.len() > 3 {
        return format_error(KvError::ExtraArgument);
    }
    let Some(k) = parts.get(1) else {
        return format_error(KvError::MissingArgument);
    };
    let key = k.replace("\"", "\\\"");
    let Some(v) = parts.get(2) else {
        if writeln!(file, "set \"{}\"", key).is_err() {
            return format_error(KvError::InvalidLogFile);
        };
        storage.remove(&key);
        return "OK".to_string();
    };
    let value = v.replace("\"", "\\\"");
    if writeln!(file, "set \"{}\" \"{}\"", key, value).is_err() {
        return format_error(KvError::InvalidLogFile);
    };
    storage.set(key.to_string(), value.to_string());
    "OK".to_string()
}

/// Devuelve el valor de una clave del minikv, si la clave existe
fn handle_get(parts: &[String], storage: &Minikv) -> String {
    if parts.len() < 2 {
        return format_error(KvError::MissingArgument);
    }
    if parts.len() > 2 {
        return format_error(KvError::ExtraArgument);
    }
    let Some(k) = parts.get(2) else {
        return format_error(KvError::NotFound);
    };
    match storage.get(k.to_string()) {
        Some(v) => v.to_string(),
        None => format_error(KvError::NotFound),
    }
}

/// Devuelve la cantidad de elementos en el minikv
fn length(parts: &[String], storage: &Minikv) -> String {
    if parts.len() > 1 {
        return format_error(KvError::ExtraArgument);
    }
    storage.length().to_string()
}

/// Borra el log, y carga el estado completo del minikv al archivo .data
fn handle_snapshot(log_path: &str, data_path: &str, parts: &[String], storage: &Minikv) -> String {
    if parts.len() > 1 {
        return format_error(KvError::ExtraArgument);
    }
    create_or_truncate_file(log_path.to_string(), data_path.to_string());
    let Ok(mut file) = OpenOptions::new().append(true).open(data_path) else {
        return format_error(KvError::InvalidDataFile);
    };
    for (k, v) in storage.iter() {
        let parse_k = k.replace("\"", "\\\"");
        let parse_v = v.replace("\"", "\\\"");
        if writeln!(file, "\"{}\" \"{}\"", parse_k, parse_v).is_err() {
            return format_error(KvError::InvalidDataFile);
        }
    }
    "OK".to_string()
}

/// Procesa un comando recibido del cliente y devuelve la respuesta como String
pub fn process_command(
    log_path: &str,
    data_path: &str,
    instructions: &[String],
    storage: &RwLock<Minikv>,
) -> String {
    let Some(command) = instructions.first() else {
        return format_error(KvError::MissingArgument);
    };
    match command.as_str() {
        "length" => match storage.read() {
            Ok(guard) => length(instructions, &guard),
            Err(_) => format_error(KvError::InvalidDataFile),
        },
        "get" => match storage.read() {
            Ok(guard) => handle_get(instructions, &guard),
            Err(_) => format_error(KvError::InvalidDataFile),
        },
        "set" => match storage.write() {
            Ok(mut guard) => handle_set(log_path, instructions, &mut guard),
            Err(_) => format_error(KvError::InvalidDataFile),
        },
        "snapshot" => match storage.write() {
            Ok(guard) => handle_snapshot(log_path, data_path, instructions, &guard),
            Err(_) => format_error(KvError::InvalidDataFile),
        },
        _ => format_error(KvError::UnknownCommand),
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::minikv_server::Minikv;
    use std::fs;
    use std::io::{BufRead, BufReader};
    use std::path::Path;

    #[test]
    fn test_set_log_writes_correctly() {
        let log_path = "test_set.log";
        let _ = File::create(log_path);
        let mut storage = Minikv::new();
        let parts = vec![
            "set".to_string(),
            "velez".to_string(),
            "sarsfield".to_string(),
        ];
        let res = handle_set(log_path, &parts, &mut storage);
        assert_eq!(res, "OK");
        let file = File::open(log_path).unwrap();
        let mut lines = BufReader::new(file).lines();
        let first_line = lines.next().unwrap().unwrap();
        assert_eq!(first_line, "set \"velez\" \"sarsfield\"");
        let _ = fs::remove_file(log_path);
    }

    #[test]
    fn test_create_files() {
        let log_path = "test_create.log";
        let data_path = "test_create.data";
        create_or_truncate_file(log_path.to_string(), data_path.to_string());
        assert!(Path::new(log_path).exists());
        assert!(Path::new(data_path).exists());
        let _ = fs::remove_file(log_path);
        let _ = fs::remove_file(data_path);
    }

    #[test]
    fn test_snapshot_writes_correctly() {
        let log_path = "test_snapshot.log";
        let data_path = "test_snapshot.data";
        let mut storage = Minikv::new();
        storage.insert("velez".to_string(), "sarsfield".to_string());
        let parts = vec!["snapshot".to_string()];
        let res = handle_snapshot(log_path, data_path, &parts, &storage);
        assert_eq!(res, "OK");
        let file = File::open(data_path).unwrap();
        let mut lines = BufReader::new(file).lines();
        let first_line = lines.next().unwrap().unwrap();
        assert_eq!(first_line, "\"velez\" \"sarsfield\"");
        let _ = fs::remove_file(log_path);
        let _ = fs::remove_file(data_path);
    }

    #[test]
    fn test_process_command_missing_argument() {
        let storage = RwLock::new(Minikv::new());
        let instructions = vec!["get".to_string()];
        let response = process_command("test.log", "test.data", &instructions, &storage);
        assert_eq!(response, "ERROR: MISSING ARGUMENT");
    }

    #[test]
    fn test_process_command_extra_argument() {
        let storage = RwLock::new(Minikv::new());
        let instructions = vec!["length".to_string(), "basura".to_string()];
        let response = process_command("test.log", "test.data", &instructions, &storage);
        assert_eq!(response, "ERROR: EXTRA ARGUMENT");
    }

    #[test]
    fn test_process_command_unknown_command() {
        let storage = RwLock::new(Minikv::new());
        let instructions = vec!["borrar".to_string(), "velez".to_string()];
        let response = process_command("test.log", "test.data", &instructions, &storage);
        assert_eq!(response, "ERROR: UNKNOWN COMMAND");
    }
}
