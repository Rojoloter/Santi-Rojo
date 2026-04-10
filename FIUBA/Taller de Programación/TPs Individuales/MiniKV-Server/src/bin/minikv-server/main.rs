mod main_server_fns;
mod minikv_server;

use std::sync::Arc;
use std::thread;

fn main() {
    let log_path = "./.minikv.log";
    let data_path = "./.minikv.data";
    let Some(shared_storage) = main_server_fns::initialize_storage(log_path, data_path) else {
        return;
    };
    let Some(listener) = main_server_fns::initialize_listener() else {
        return;
    };
    for stream in listener.incoming() {
        let Ok(stream) = stream else { continue };
        let storage_for_client = Arc::clone(&shared_storage);
        thread::spawn(move || {
            main_server_fns::handle_client(stream, storage_for_client, log_path, data_path);
        });
    }
}
