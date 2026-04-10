use crate::errors::KvError;
use crate::errors::print_error;
use crate::minikv;
use std::fs::{File, OpenOptions};
use std::io::{Error, Write};

/// Crea o limpia un archivo a partir de un path
pub fn create_or_truncate_file(log_path: String, data_path: String) {
    if File::create(log_path).is_err() {
        print_error(KvError::InvalidLogFile)
    };
    if File::create(data_path).is_err() {
        print_error(KvError::InvalidDataFile)
    };
}

/// Escribe la clave - valor en el log, siempre entre comillas "
pub fn set_in_log(log_path: String, parts: Vec<String>) -> Result<(), Error> {
    let mut file = OpenOptions::new().append(true).open(log_path)?;
    if parts.len() <= 2 {
        print_error(KvError::MissingArgument);
        return Ok(());
    } else if parts.len() > 4 {
        print_error(KvError::ExtraArgument);
        return Ok(());
    }
    let Some(k) = parts.get(2) else {
        print_error(KvError::MissingArgument);
        return Ok(());
    };
    let key = k.replace("\"", "\\\"");
    let Some(v) = parts.get(3) else {
        writeln!(file, "set \"{}\"", key)?;
        println!("OK");
        return Ok(());
    };
    let value = v.replace("\"", "\\\"");
    writeln!(file, "set \"{}\" \"{}\"", key, value)?;
    println!("OK");
    Ok(())
}

/// Devuelve el valor de una clave del minikv, si la clave existe
pub fn get_from_memory(parts: Vec<String>, storage: minikv::Minikv) {
    if parts.len() == 3 {
        let Some(k) = parts.get(2) else {
            print_error(KvError::NotFound);
            return;
        };
        match storage.get(k.to_string()) {
            Some(v) => println!("{}", v),
            None => print_error(KvError::NotFound),
        }
    } else if parts.len() < 3 {
        print_error(KvError::MissingArgument);
    } else {
        print_error(KvError::ExtraArgument);
    }
}

/// Borra el log, y carga el estado completo del minikv al archivo .data
pub fn snapshot(log_path: String, data_path: String, storage: minikv::Minikv) -> Result<(), Error> {
    let data_file = data_path.clone();
    create_or_truncate_file(log_path, data_path);
    let mut file = OpenOptions::new().append(true).open(data_file)?;
    for (k, v) in storage.iter() {
        let parse_k = k.replace("\"", "\\\"");
        let parse_v = v.replace("\"", "\\\"");
        writeln!(file, "\"{}\" \"{}\"", parse_k, parse_v)?;
    }
    println!("OK");
    Ok(())
}

/// Wrapper para las distintas funciones de comandos (length, get, set y snapshot)
pub fn make_command(
    log_path: String,
    data_path: String,
    instructions: Vec<String>,
    storage: minikv::Minikv,
) -> Result<(), Error> {
    let Some(command) = instructions.get(1) else {
        print_error(KvError::MissingArgument);
        return Ok(());
    };

    match command.as_str() {
        "length" | "snapshot" if instructions.len() > 2 => {
            print_error(KvError::ExtraArgument);
            return Ok(());
        }
        "length" => println!("{}", storage.length()),
        "get" => get_from_memory(instructions, storage),
        "set" => return set_in_log(log_path, instructions),
        "snapshot" => snapshot(log_path, data_path, storage)?,
        _ => print_error(KvError::UnknownCommand),
    }

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::minikv::Minikv;
    use std::fs;
    use std::io::{BufRead, BufReader};
    use std::path::Path;

    #[test]
    fn test_set_log_writes_correctly() {
        let log_path = "test_set.log".to_string();
        let _ = File::create(&log_path).unwrap();
        let parts = vec![
            " ".to_string(),
            "set".to_string(),
            "velez".to_string(),
            "sarsfield".to_string(),
        ];
        let res = set_in_log(log_path.clone(), parts);
        assert!(res.is_ok());
        let file = File::open(&log_path).unwrap();
        let mut lines = BufReader::new(file).lines();
        let first_line = lines.next().unwrap().unwrap();
        assert_eq!(first_line, "set \"velez\" \"sarsfield\"");
        let _ = fs::remove_file(&log_path);
    }

    #[test]
    fn test_create_files() {
        let log_path = "test_create.log".to_string();
        let data_path = "test_create.data".to_string();
        create_or_truncate_file(log_path.clone(), data_path.clone());
        assert!(Path::new(&log_path).exists());
        assert!(Path::new(&data_path).exists());
        let _ = fs::remove_file(&log_path);
        let _ = fs::remove_file(&data_path);
    }

    #[test]
    fn test_snapshot_writes_correctly() {
        let log_path = "test_snapshot.log".to_string();
        let data_path = "test_snapshot.data".to_string();
        let mut storage = Minikv::new();
        storage.insert("velez".to_string(), "sarsfield".to_string());
        let res = snapshot(log_path.clone(), data_path.clone(), storage);
        assert!(res.is_ok());
        let file = File::open(&data_path).unwrap();
        let mut lines = BufReader::new(file).lines();
        let first_line = lines.next().unwrap().unwrap();
        assert_eq!(first_line, "\"velez\" \"sarsfield\"");
        let _ = fs::remove_file(&log_path);
        let _ = fs::remove_file(&data_path);
    }
}
