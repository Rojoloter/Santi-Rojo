mod errors;
mod main_fns;
mod minikv;

use crate::errors::{KvError, print_error};
use std::env;
use std::path::Path;

fn main() {
    let log_path = "./.minikv.log";
    let data_path = "./.minikv.data";
    if !Path::new(log_path).exists() || !Path::new(data_path).exists() {
        main_fns::create_or_truncate_file(log_path.to_string(), data_path.to_string());
    }
    let mut storage = minikv::Minikv::new();
    let arguments: Vec<String> = env::args().collect();
    if storage
        .load_from_file(data_path.to_string(), false)
        .is_err()
    {
        return;
    };
    if storage.load_from_file(log_path.to_string(), true).is_err() {
        return;
    };
    if main_fns::make_command(
        log_path.to_string(),
        data_path.to_string(),
        arguments,
        storage,
    )
    .is_err()
    {
        print_error(KvError::UnknownCommand)
    }
}
