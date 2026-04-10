pub enum KvError {
    NotFound,
    ExtraArgument,
    InvalidDataFile,
    InvalidLogFile,
    MissingArgument,
    UnknownCommand,
}

pub fn print_error(e: KvError) {
    let err = match e {
        KvError::NotFound => "NOT FOUND",
        KvError::ExtraArgument => "EXTRA ARGUMENT",
        KvError::InvalidDataFile => "INVALID DATA FILE",
        KvError::InvalidLogFile => "INVALID LOG FILE",
        KvError::MissingArgument => "MISSING ARGUMENT",
        KvError::UnknownCommand => "UNKNOWN COMMAND",
    };
    println!("ERROR: {}", err)
}
