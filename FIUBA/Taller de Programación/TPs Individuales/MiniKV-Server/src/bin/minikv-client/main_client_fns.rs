use minikv::errors::{KvError, print_error};
use std::io;
use std::io::{BufRead, BufReader, Error, Stdin, Write};
use std::net::TcpStream;
use std::sync::Arc;

pub const READ_TIMEOUT: u64 = 5;
pub const WRITE_TIMEOUT: u64 = 5;

/// Verifica que se haya ingresado un solo argumento, y devuelve la dirección IP
pub fn get_address(args: &[String]) -> Result<String, Error> {
    if args.len() > 2 {
        print_error(KvError::ExtraArgument);
        return Err(Error::new(io::ErrorKind::InvalidData, ""));
    }
    let Some(address) = args.get(1) else {
        print_error(KvError::MissingArgument);
        return Err(Error::new(io::ErrorKind::InvalidData, ""));
    };
    Ok(address.to_string())
}

/// Lee la entrada del standard input, la manda al servidor e imprime la respuesta
pub fn main_loop(
    shared_stream: Arc<TcpStream>,
    stdin: Stdin,
    mut input: String,
    mut response: String,
) {
    let mut server_reader = BufReader::new(&*shared_stream);
    loop {
        input.clear();
        match stdin.read_line(&mut input) {
            Ok(0) => return,
            Ok(_) => {}
            Err(_) => {
                print_error(KvError::InvalidArgs);
                return;
            }
        }
        if input.trim().is_empty() {
            continue;
        }
        if (&*shared_stream).write_all(input.as_bytes()).is_err() {
            print_error(KvError::ClientSocketBinding);
            return;
        }
        response.clear();
        match server_reader.read_line(&mut response) {
            Ok(0) => return,
            Ok(_) => print!("{}", response),
            Err(_) => {
                print_error(KvError::Timeout);
                return;
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_get_address_valid_arguments() {
        let args = vec![
            "target/debug/minikv-client".to_string(),
            "127.0.0.1:12345".to_string(),
        ];
        let result = get_address(&args);
        assert!(result.is_ok());
        assert_eq!(result.unwrap(), "127.0.0.1:12345");
    }

    #[test]
    fn test_get_address_missing_argument() {
        let args = vec!["target/debug/minikv-client".to_string()];
        let result = get_address(&args);
        assert!(result.is_err());
    }

    #[test]
    fn test_get_address_extra_arguments() {
        let args = vec![
            "target/debug/minikv-client".to_string(),
            "127.0.0.1:12345".to_string(),
            "set".to_string(),
        ];
        let result = get_address(&args);
        assert!(result.is_err());
    }
}
