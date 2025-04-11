function login() {
    const usuario = document.getElementById("txtUser").value.trim()
    const passwordIn = document.getElementById("txtPassword").value.trim()
   
    if (!usuario || !passwordIn) {
        swal.fire("Error", "Por favor, completa todos los campos", "error");
        return;
    }

    const url = "/instructorLogin"
    const loginData = {
        email: usuario,
        password: passwordIn,
      
    }
    console.log("datos enviados", loginData);

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(loginData)
    })
        .then(respuesta => respuesta.json())
        .then(resultado => {
            console.log("esta es la data; ", resultado.message)
            if (resultado.message == "Login exitoso") {
                swal.fire("Iniciando Sesion", resultado.message, "success")
                setTimeout(function () {
                    location.href = "/dash"
                }, 2000)
            } else {
                if (resultado.message == "Contraseña incorrecta") {
                    swal.fire("Error", resultado.message, "error")
                    alert("Contraseña incorrecta")
                } else if (resultado.message == "Usuario no registrado") {
                    swal.fire("Error", resultado.message, "error")
                    alert("Usuario no encontrado")
                }
                swal.fire("Error", resultado.message, "error")
            }
        })
        .catch(error => {
            console.log("el error es: ", error)
            alert("Error al iniciar sesión del catch")
        })
}

function eliminarGuia() {
    Swal.fire({
        title: '¿Estás seguro?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33', // rojo
        cancelButtonColor: '#6c757d', // gris bootstrap
        confirmButtonText: 'Sí, eliminar',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            const url = "/generos/" + codigo
            fetch(url, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(respuesta =>{
                Swal.fire(
                    '¡Eliminado!',
                    'La guía ha sido eliminada.',
                    'success'
                ).then(() => {
                    location.href = "/guiasVista"
                })
            } )
            .catch(error => {
                Swal.fire('Error', 'Error de conexión.', 'error');
                console.log(error)
            });
        }
    });
}


function salir() {
    const url = "/usuarios/logout"
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(respuesta => respuesta.json())
        .then(resultado => {
            console.log("esta es la data; ", resultado)
            if (resultado.message == "Sesión cerrada") {
                location.href = "/loginVista"
                alert("Sesion cerrada")
            } else {
                swal.fire("Error", resultado.message, "error")
                alert("Error al cerrar la sesion")
            }
        })
        .catch(error => {
            console.log(error)
            alert("Error al cerrar la sesion")
        })
}
