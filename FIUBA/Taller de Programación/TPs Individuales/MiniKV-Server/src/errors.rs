pub enum KvError {
    NotFound,
    ExtraArgument,
    InvalidDataFile,
    InvalidLogFile,
    MissingArgument,
    UnknownCommand,
    InvalidArgs,
    ServerSocketBinding,
    Timeout,
    ConnectionClosed,
    ClientSocketBinding,
}

pub fn format_error(e: KvError) -> String {
    let err = match e {
        KvError::NotFound => "NOT FOUND",
        KvError::ExtraArgument => "EXTRA ARGUMENT",
        KvError::InvalidDataFile => "INVALID DATA FILE",
        KvError::InvalidLogFile => "INVALID LOG FILE",
        KvError::MissingArgument => "MISSING ARGUMENT",
        KvError::UnknownCommand => "UNKNOWN COMMAND",
        KvError::InvalidArgs => "INVALID ARGS",
        KvError::ServerSocketBinding => "SERVER SOCKET BINDING",
        KvError::Timeout => "TIMEOUT",
        KvError::ConnectionClosed => "CONNECTION CLOSED",
        KvError::ClientSocketBinding => "CLIENT SOCKET BINDING",
    };
    format!("ERROR: {}", err)
}

pub fn print_error(e: KvError) {
    println!("{}", format_error(e))
}
