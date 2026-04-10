(ns bf.core)

(defn armar-matriz [file]
  (let [contenido (clojure.string/split-lines (slurp file))
        filas-completas (map #(vec (take 80 (concat % (repeat \space)))) contenido) ;; Completa cada fila a 80 columnas
        matriz-completa (vec (take 25 (concat filas-completas (repeat (vec (repeat 80 \space))))))] ;; Completa a 25 filas
    matriz-completa))


(defn mover-pc [pc]
  (let [{:keys [x y dx dy stringmode]} pc                   ;;Desestructurar el diccionario pc
        x-max 79                 ;;Ancho maximo - 1
        y-max 24                          ;;Largo maximo - 1
        new-x (+ x dx)                                      ;;Nuevo valor X dependiendo de adónde apunta el pc
        new-y (+ y dy)                                      ;;Idem Y
        x-fin (cond
                (< new-x 0) x-max
                (> new-x x-max) 0
                :else new-x)                                ;;Verifica si hace falta pegar la vuelta en el toroide
        y-fin (cond
                (< new-y 0) y-max
                (> new-y y-max) 0
                :else new-y)]

    {:x          x-fin                                      ;;Devuelve el diccionario con los nuevos valores
     :y          y-fin
     :dx         dx
     :dy         dy
     :stringmode stringmode}))

(defn leerMatriz [matriz pila pc]
  (let
    [comando (get-in matriz [(pc :y) (pc :x)])]
    (cond
      (Character/isDigit comando)                           ;Digitos del 0-9 para apilar numeros
      (recur matriz (cons (Character/getNumericValue comando) pila) (mover-pc pc))

      (and (:stringmode pc) (not= comando \"))              ;Apilar ASCII si esta en stringmode
      (recur matriz (cons (int comando) pila) (mover-pc pc))

      :else
      (case comando
        \@ nil                                              ;Fin del programa

        ;operaciones aritmeticas
        \+ (let [a (nth pila 0 0)
                 b (nth pila 1 0)
                 cola (drop 2 pila)]
             (recur matriz (cons (+ b a) cola) (mover-pc pc)))

        \- (let [a (nth pila 0 0)
                 b (nth pila 1 0)
                 cola (drop 2 pila)]
             (recur matriz (cons (- b a) cola) (mover-pc pc)))
        \* (let [a (nth pila 0 0)
                 b (nth pila 1 0)
                 cola (drop 2 pila)]
             (recur matriz (cons (* b a) cola) (mover-pc pc)))

        \/ (let [a (nth pila 0 0)
                 b (nth pila 1 0)
                 cola (drop 2 pila)]
             (if ((comp not zero?) a)
               (recur matriz (cons (quot b a) cola) (mover-pc pc))))
        \% (let [a (nth pila 0 0)
                 b (nth pila 1 0)
                 cola (drop 2 pila)]
             (if ((comp not zero?) a)
               (recur matriz (cons (mod b a) cola) (mover-pc pc))))
        ;cambiar direccion del PC
        \> (recur matriz pila (mover-pc {:x (pc :x) :y (pc :y) :dx 1 :dy 0 :stringmode (pc :stringmode)}))
        \< (recur matriz pila (mover-pc {:x (pc :x) :y (pc :y) :dx -1 :dy 0 :stringmode (pc :stringmode)}))
        \v (recur matriz pila (mover-pc {:x (pc :x) :y (pc :y) :dx 0 :dy 1 :stringmode (pc :stringmode)}))
        \^ (recur matriz pila (mover-pc {:x (pc :x) :y (pc :y) :dx 0 :dy -1 :stringmode (pc :stringmode)}))
        \? (let [direccion (rand-nth [{:dx 1 :dy 0} {:dx -1 :dy 0} {:dx 0 :dy 1} {:dx 0 :dy -1}])]
             (recur matriz pila (mover-pc (merge pc direccion))))

        \! (let [a (nth pila 0 0)]
             (recur matriz (cons (if (zero? a) 1 0) (rest pila)) (mover-pc pc)));Negacion logica

        \` (let [a (nth pila 0 0)
                 b (nth pila 1 0)
                 cola (drop 2 pila)]
             (recur matriz (cons (if (> b a) 1 0) cola) (mover-pc pc)))   ; Mayor

        ;IFs
        \_ (recur matriz (rest pila) (if (zero? (nth pila 0 0))
                                              (mover-pc (assoc pc :dx 1 :dy 0))
                                              (mover-pc (assoc pc :dx -1 :dy 0))))
        \| (recur matriz (rest pila) (if (zero? (nth pila 0 0))
                                              (mover-pc (assoc pc :dx 0 :dy 1))
                                              (mover-pc (assoc pc :dx 0 :dy -1))))

        \: (recur matriz (cons (nth pila 0 0) pila) (mover-pc pc)) ;Duplicar tope
        \\ (let [a (nth pila 0 0)
                 b (nth pila 1 0)
                 cola (drop 2 pila)]
             (recur matriz (cons b (cons a cola)) (mover-pc pc)))       ;Dar vuelta primero y segundo
        \$ (recur matriz (rest pila) (mover-pc pc)) ;Desapilar
        \# (recur matriz pila (mover-pc (mover-pc pc))) ; Saltear comando

        \. (do                                              ;Imprimir int
             (print (nth pila 0 0))
             (recur matriz (rest pila) (mover-pc pc)))
        \, (do                                              ;Imprimir char
             (print (char (nth pila 0 0)))
             (flush)
             (recur matriz (rest pila) (mover-pc pc)))

        \" (if (:stringmode pc)                             ;Entrar y salir de stringmode
             (recur matriz pila (assoc (mover-pc pc) :stringmode false))
             (recur matriz pila (assoc (mover-pc pc) :stringmode true)))

        \g (let [a (nth pila 0 0)     ;Obtener un espacio de la matriz
                 b (nth pila 1 0)
                 cola (drop 2 pila)]
             (recur matriz
                    (if (and (< a 25) (< b 80))
                             (cons (int(get-in matriz [a b]))  cola)
                             (cons 0 cola))
                    (mover-pc pc)))


        \p (let [a (nth pila 0 0)   ;Colocar un elemento en un lugar de la matriz
                 b (nth pila 1 0)
                 cola (drop 2 pila)]
             (recur (assoc-in matriz [(mod a 25) (mod b 80)] (char (first cola))) (rest cola) (mover-pc pc)))

        \~ (let [input (read)]                              ;Input int
             (recur matriz (cons input pila) (mover-pc pc)))
        \& (let [input (char (read))]                       ;Input char
             (recur matriz (cons (int input) pila) (mover-pc pc)))

        (recur matriz pila (mover-pc pc))            ;Espacio vacio, Default
        ))))

(defn -main [file]
  (let [matriz (armar-matriz file)
        pila '()
        pc {:x 0 :y 0 :dx 1 :dy 0 :stringmode false}]
    (leerMatriz matriz pila pc)))
;your code here