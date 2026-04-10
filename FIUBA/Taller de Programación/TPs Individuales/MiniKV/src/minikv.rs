use crate::errors::{KvError, print_error};
use std::collections::HashMap;
use std::fs::File;
use std::io::{BufRead, BufReader, Error};

/// Almacenamiento en memoria de los datos. Usa un hashmap para guardar la clave - valor
pub struct Minikv {
    memory: HashMap<String, String>,
}

impl Minikv {
    pub fn new() -> Self {
        Minikv {
            memory: HashMap::new(),
        }
    }

    /// Separa las claves y valores por comillas ". Permite que hayan comillas dentro de las claves/valores
    /// si estan escapadas con \
    fn split_words(args: String) -> Vec<String> {
        let (mut res, mut current_word) = (Vec::<String>::new(), String::new());
        let (mut in_quotation, mut escaped) = (false, false);
        for c in args.chars() {
            if escaped {
                current_word.push(c);
                escaped = false;
                continue;
            }
            if c == '\\' {
                escaped = true;
                continue;
            }
            if c == '"' {
                in_quotation = !in_quotation;
                continue;
            }
            if c == ' ' && !in_quotation && !current_word.is_empty() {
                res.push(current_word.clone());
                current_word.clear();
            }
            if c != ' ' || in_quotation {
                current_word.push(c);
            }
        }
        if !current_word.is_empty() {
            res.push(current_word.clone());
        }
        res
    }

    /// Carga los datos del archivo .log al HashMap
    fn load_from_log(&mut self, parts: Vec<String>, command: &String) -> Result<(), Error> {
        if parts.is_empty() || command != "set" || parts.len() > 3 {
            print_error(KvError::InvalidLogFile);
            return Err(Error::new(std::io::ErrorKind::InvalidData, ""));
        }
        let Some(k) = parts.get(1) else {
            print_error(KvError::InvalidLogFile);
            return Err(Error::new(std::io::ErrorKind::InvalidData, ""));
        };
        let Some(v) = parts.get(2) else {
            self.memory.remove(k);
            return Ok(());
        };
        self.memory.insert(k.clone(), v.clone());
        Ok(())
    }

    /// Carga los datos del archivo .data al HashMap
    fn load_from_data(&mut self, parts: Vec<String>, command: &String) -> Result<(), Error> {
        if parts.len() != 2 || command == "set" {
            print_error(KvError::InvalidDataFile);
            return Err(Error::new(std::io::ErrorKind::InvalidData, ""));
        }
        let Some(k) = parts.first() else {
            print_error(KvError::InvalidDataFile);
            return Err(Error::new(std::io::ErrorKind::InvalidData, ""));
        };
        let Some(v) = parts.get(1) else {
            print_error(KvError::InvalidDataFile);
            return Err(Error::new(std::io::ErrorKind::InvalidData, ""));
        };
        self.memory.insert(k.clone(), v.clone());
        Ok(())
    }

    /// Arma el HashMap con las claves y valores a partir de los distintos archivos.
    /// Recibe un bool para distinguir entre log y data
    pub fn load_from_file(&mut self, path: String, is_log: bool) -> Result<(), Error> {
        let file = File::open(path)?;
        let reader = BufReader::new(file);
        for line in reader.lines() {
            let line = line?;
            let parts = Self::split_words(line);
            let Some(command) = parts.first() else {
                print_error(KvError::MissingArgument);
                return Err(Error::new(std::io::ErrorKind::InvalidData, ""));
            };
            if is_log {
                self.load_from_log(parts.clone(), command)?;
            } else {
                self.load_from_data(parts.clone(), command)?;
            }
        }
        Ok(())
    }

    /// Devuelve la cantidad de elementos en el minikv
    pub fn length(&self) -> usize {
        self.memory.len()
    }

    /// Devuelve el valor de una clave del minikv, si la clave existe
    pub fn get(&self, key: String) -> Option<String> {
        self.memory.get(&key).map(|v| v.to_string())
    }

    /// Devuelve un iterador del hashmap interno
    pub fn iter(&self) -> impl Iterator<Item = (&String, &String)> {
        self.memory.iter()
    }

    #[cfg(test)]
    pub fn insert(&mut self, k: String, v: String) {
        self.memory.insert(k, v);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_get_correct_value_if_key_exists() {
        let mut storage = Minikv::new();
        storage
            .memory
            .insert("velez".to_string(), "sarsfield".to_string());
        let res = storage.get("velez".to_string());
        assert_eq!(res, Some("sarsfield".to_string()))
    }

    #[test]
    fn test_get_none_if_key_doesnt_exists() {
        let storage = Minikv::new();
        let res = storage.get("velez".to_string());
        assert_eq!(res, None)
    }

    #[test]
    fn test_len_on_empty_hash() {
        let storage = Minikv::new();
        let len = storage.length();
        assert_eq!(len, 0);
    }

    #[test]
    fn test_len_on_hash_with_elements() {
        let mut storage = Minikv::new();
        storage
            .memory
            .insert("velez".to_string(), "sarsfield".to_string());
        storage
            .memory
            .insert("jose".to_string(), "amalfitani".to_string());
        storage
            .memory
            .insert("tanque".to_string(), "silva".to_string());
        let len = storage.length();
        assert_eq!(len, 3);
    }

    #[test]
    fn test_overwrite_value() {
        let mut storage = Minikv::new();
        storage
            .memory
            .insert("tecnico".to_string(), "bianchi".to_string());
        storage
            .memory
            .insert("tecnico".to_string(), "gareca".to_string());
        assert_eq!(
            storage.get("tecnico".to_string()),
            Some("gareca".to_string())
        );
        let len = storage.length();
        assert_eq!(len, 1);
    }

    #[test]
    fn test_remove_existent_element() {
        let mut storage = Minikv::new();
        storage
            .memory
            .insert("velez".to_string(), "sarsfield".to_string());
        storage.memory.remove("velez");
        let len = storage.length();
        assert_eq!(len, 0);
        assert_eq!(storage.get("velez".to_string()), None);
    }

    #[test]
    fn test_remove_non_existent_element() {
        let mut storage = Minikv::new();
        storage
            .memory
            .insert("velez".to_string(), "sarsfield".to_string());
        storage.memory.remove("river");
        let len = storage.length();
        assert_eq!(len, 1);
        assert_eq!(
            storage.get("velez".to_string()),
            Some("sarsfield".to_string())
        );
    }

    #[test]
    fn test_empty_strings() {
        let mut storage = Minikv::new();
        storage.memory.insert("velez".to_string(), "".to_string());
        let len = storage.length();
        assert_eq!(len, 1);
        assert_eq!(storage.get("velez".to_string()), Some("".to_string()));
        storage.memory.insert("".to_string(), "velez".to_string());
        let len = storage.length();
        assert_eq!(len, 2);
        assert_eq!(storage.get("".to_string()), Some("velez".to_string()));
    }

    #[test]
    fn test_iter_has_all_elements() {
        let mut storage = Minikv::new();
        storage
            .memory
            .insert("velez".to_string(), "sarsfield".to_string());
        storage
            .memory
            .insert("jose".to_string(), "amalfitani".to_string());
        storage
            .memory
            .insert("ricardo".to_string(), "gareca".to_string());
        let iter = storage.iter();
        let len = iter.count();
        assert_eq!(len, 3);
    }
}
