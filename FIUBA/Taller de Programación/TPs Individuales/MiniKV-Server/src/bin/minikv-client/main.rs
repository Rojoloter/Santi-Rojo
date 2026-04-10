mod main_client_fns;

use minikv::errors::{KvError, print_error};
use std::io;
use std::net::TcpStream;
use std::sync::Arc;
use std::time::Duration;

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let Ok(address) = main_client_fns::get_address(&args) else {
        return;
    };
    let Ok(stream) = TcpStream::connect(address.as_str()) else {
        print_error(KvError::ClientSocketBinding);
        return;
    };
    let read_timeout = Duration::from_secs(main_client_fns::READ_TIMEOUT);
    let write_timeout = Duration::from_secs(main_client_fns::WRITE_TIMEOUT);
    if stream.set_read_timeout(Some(read_timeout)).is_err() {
        print_error(KvError::ClientSocketBinding);
        return;
    }
    if stream.set_write_timeout(Some(write_timeout)).is_err() {
        print_error(KvError::ClientSocketBinding);
        return;
    }
    let shared_stream = Arc::new(stream);
    let stdin = io::stdin();
    let input = String::new();
    let response = String::new();
    main_client_fns::main_loop(shared_stream, stdin, input, response)
}
