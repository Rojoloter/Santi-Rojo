from flask import Flask, render_template, redirect, url_for, request
import requests
import json

app = Flask(__name__)

@app.errorhandler(400)
def bad_request(e):
    return render_template("400.html"), 400

@app.errorhandler(403)
def forbidden_error(e):
    return render_template("403.html"), 403


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(e):
    return render_template("500.html") , 500


@app.route("/about_us")
def about_us():
    return render_template("about_us.html")

def data_return(tipo):
    if tipo == "voluntario":
        return (request.form.get("fnombre_voluntario"),
                request.form.get("fpuesto_voluntario"),
                request.form.get("ftelefono_voluntario"),
                request.form.get("fcuil_voluntario"),
                request.form.get("ffoto_voluntario"),
                request.form.get("frefugio_a_servir")
                )
    elif tipo == "refugio":
        calle = request.form.get("fdireccion_refugio")
        barrio = request.form.get("fbarrio_refugio")
        ciudad = request.form.get("fciudad_refugio")
        postal = request.form.get("fpostal_refugio")
        pais = request.form.get("fpais_refugio")
        direccion = [calle, barrio, ciudad, postal, pais]
        direccion = ", ".join(direccion) #SE JUNTAN LOS DATOS DE LA DIRECCION CON COMA PARA SER UTILIZADO POR MAPBOX
        return (request.form.get("fnombre_refugio"),
                direccion,
                request.form.get("fdescripcion_refugio"),
                request.form.get("ftipo_refugio"),
                request.form.get("ftelefono_refugio"),
                request.form.get("fusuario_refugio"),
                request.form.get("fimagen_refugio"))

@app.route("/voluntario_cargado", methods = ["GET","POST"])
def cargar_voluntario():
    if request.method == "POST":
        nombre, puesto, telefono, cuil, foto, refugio = data_return("voluntario")
        datos = {
            "nombre": nombre,
            "puesto": puesto,
            "telefono": telefono,
            'cuil_voluntario': int(cuil),
            'link_foto': foto,
            'nombre_refugio': refugio
        }
        data_json = json.dumps(datos)
        URL = "http://pedrogillen.pythonanywhere.com/crear_voluntario"
        res = requests.post(URL, data=data_json, headers={'Content-Type': 'application/json'})
        #Falta decidir que hacer dependiendo de la response
        return redirect(url_for("feed"))
    return render_template("cargar_voluntario.html")


@app.route("/edicion_refugio/<id>",methods = ["GET","POST"])
def edicion_refugio(id):
    if request.method == "POST":
        nombre_refugio, direccion, descripcion, tipo, telefono, usuario, foto = data_return("refugio")
        datos = {
            "nombre_refugio": nombre_refugio,
            "direccion": direccion,
            "descripcion": descripcion,
            "tipo_refugio": tipo,
            "telefono": telefono,
            "link_foto": foto
        }
        datos_json = json.dumps(datos)
        URL = "http://pedrogillen.pythonanywhere.com/refugios/"+id
        res = requests.patch(URL, data=datos_json, headers={'Content-Type': 'application/json'})
        if res.status_code == 200:
            return redirect(url_for('detalles_refugio', id=id))
    return render_template("editar_refugio.html", id=id)

@app.route("/edicion_voluntario/<cuil>", methods = ["GET","POST"])
def edicion_voluntario(cuil):
    if request.method == "POST":
        nombre, puesto, telefono, cuil_vol, foto, refugio = data_return("voluntario")
        URL = "http://pedrogillen.pythonanywhere.com/modificar_voluntario/" + cuil
        datos = {
            "nombre": nombre,
            "puesto": puesto,
            "telefono": telefono,
            'cuil_voluntario': cuil,
            'foto': foto,
            'nombre_refugio': refugio,
        }
        res = requests.patch(URL, data=json.dumps(datos), headers={'Content-Type': 'application/json'})
        return redirect(url_for('detalles_voluntario', cuil=cuil))
    return render_template("editar_voluntario.html", cuil=cuil)

@app.route("/detalles_voluntario/<cuil>")
def detalles_voluntario(cuil):
    URL = "http://pedrogillen.pythonanywhere.com/obtener_voluntario/" + cuil
    res = requests.get(URL)
    data = json.loads(res.text)
    datos = data['data']
    return render_template("detalles_voluntario.html", data=datos, cuil=cuil)

@app.route("/detalles_refugio/<id>")
def detalles_refugio(id):
    URL = "http://pedrogillen.pythonanywhere.com/obtener_refugio/" + id
    res = requests.get(URL)
    data = json.loads(res.text)
    refugio = data['data_refugio']
    voluntarios = data['voluntarios']
    return render_template("detalles_refugio.html", refugio=refugio, voluntarios=voluntarios)

@app.route("/", methods=["GET", "POST"])
def feed():
    URL = "http://pedrogillen.pythonanywhere.com/obtener_refugios"
    result = requests.get(URL)
    refugios = json.loads(result.text)
    if request.method == "POST":
        refugios_filtrados = []
        filtro = request.form.get("fsearch_input")
        for refugio in refugios:
            if (filtro.lower() in refugio["nombre"].lower()) or (filtro.lower() in refugio["tipo"].lower()):
                refugios_filtrados.append(refugio)
        return render_template("feed.html", refugios=refugios_filtrados)
    return render_template("feed.html", refugios=refugios)

@app.route("/cargar_refugio", methods = ["GET","POST"])
def cargar_refugio():
    if request.method == "POST":
        nombre_refugio, direccion, descripcion, tipo, telefono, usuario, foto = data_return("refugio")
        datos = {
            "nombre_refugio": nombre_refugio,
            "direccion": direccion,
            "descripcion": descripcion,
            "tipo_refugio": tipo,
            "telefono": telefono,
            "link_foto": foto
        }
        datos_json = json.dumps(datos)
        URL = "http://pedrogillen.pythonanywhere.com/crear_refugio"
        result = requests.post(URL, data=datos_json, headers={'Content-Type': 'application/json'})
        return redirect("/feed")
    return render_template("cargar_refugio.html")


@app.route("/mapa")
def mapa():
    return render_template("mapa.html")


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)