document.addEventListener("DOMContentLoaded", () => {

    const toggle = document.getElementById("menu-toggle");
    const menu = document.getElementById("nav-menu");
    const track = document.getElementById("track");

    toggle.addEventListener("click", () => {
        menu.classList.toggle("active");
    });

    // navbar scroll
    window.addEventListener("scroll", () => {
        const nav = document.querySelector(".navbar");

        if (window.scrollY > 50){
            nav.classList.add("scrolled");
        } else{
            nav.classList.remove("scrolled");
        }
    });

    // animaciones
    const reveals = document.querySelectorAll(".reveal-left, .reveal-right");

    function activarAnimaciones() {
        const triggerBottom = window.innerHeight * 0.85;

        reveals.forEach(el => {
            const boxTop = el.getBoundingClientRect().top;

            if (boxTop < triggerBottom) {
                el.classList.add("active");
            }
        });
    }

    window.addEventListener("scroll", activarAnimaciones);
    activarAnimaciones();

    // animacion del mapa
    const mapa = document.querySelector(".mapa");
    const info = document.querySelector(".info");

    function mostrarElementos() {
        const trigger = window.innerHeight * 0.85;

        const mapaTop = mapa.getBoundingClientRect().top;
        const infoTop = info.getBoundingClientRect().top;

        if (mapaTop < trigger) {
            mapa.classList.add("show");
        }

        if (infoTop < trigger) {
            info.classList.add("show");
        }
    }

    window.addEventListener("scroll", mostrarElementos);
    mostrarElementos();
});


function enviarTestimonio(){

    const nombre = document.getElementById("nombre");
    const comentario = document.getElementById("comentario");

    // VALIDACIONES
    if(nombre.value.trim() === ""){
        mostrarMensajeTestimonio("⚠️ Ingresa tu nombre", "error");
        nombre.focus();
        return;
    }

    if(comentario.value.trim() === ""){
        mostrarMensajeTestimonio("⚠️ Escribe un comentario", "error");
        comentario.focus();
        return;
    }

    if(estrellasSeleccionadas === 0){
        mostrarMensajeTestimonio("⭐ Selecciona una calificación", "error");
        return;
    }

    // ENVÍO
    fetch("/crear_testimonio", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            nombre: nombre.value,
            comentario: comentario.value,
            estrellas: estrellasSeleccionadas
        })
    })
    .then(res => res.json())
    .then(data => {

        if(data.error){
            mostrarMensajeTestimonio(data.error, "error");
            return;
        }

        // LIMPIAR FORM
        nombre.value = "";
        comentario.value = "";

        estrellasSeleccionadas = 0;
        document.querySelectorAll(".rating i").forEach(star => {
            star.classList.remove("active");
        });

        cargarTestimonios();

        mostrarMensajeTestimonio("✅ Gracias por tu opinión", "success");
    })
    .catch(() => {
        mostrarMensajeTestimonio("❌ Error al enviar", "error");
    });
}


function cargarTestimonios(){
    fetch("/testimonios")
    .then(res => res.json())
    .then(data => {

        const track = document.getElementById("track");
        track.innerHTML = "";

        data.forEach(t => {

            let estrellas = "⭐".repeat(t.estrellas);
            let inicial = t.nombre.charAt(0).toUpperCase();

            const div = document.createElement("div");
            div.classList.add("testimonio-card");

            div.innerHTML = `
                <div class="testimonio-header">
                    <div class="avatar">${inicial}</div>
                    <h4>${t.nombre}</h4>
                </div>

                <div class="estrellas">${estrellas}</div>
                <p>"${t.comentario}"</p>
            `;

            track.appendChild(div);
        });
    });
}


// cargar testimonios al inicio
window.addEventListener("load", cargarTestimonios);


// estrellas
let estrellasSeleccionadas = 0;

const stars = document.querySelectorAll(".rating i");

stars.forEach(star => {
    star.addEventListener("click", () => {
        estrellasSeleccionadas = star.getAttribute("data-value");

        stars.forEach(s => s.classList.remove("active"));

        for(let i = 0; i < estrellasSeleccionadas; i++){
            stars[i].classList.add("active");
        }
    });
});


// animacion formulario
const formBox = document.querySelector(".form-box");

function mostrarFormulario(){
    const trigger = window.innerHeight * 0.85;
    const top = formBox.getBoundingClientRect().top;

    if(top < trigger){
        formBox.classList.add("active");
    }
}

window.addEventListener("scroll", mostrarFormulario);
window.addEventListener("load", mostrarFormulario);


// carrusel
let index = 0;

function moverCarrusel(){
    const track = document.getElementById("track");
    const cards = document.querySelectorAll(".testimonio-card");

    if(cards.length === 0) return;

    index++;

    if(index >= cards.length){
        index = 0;
    }

    track.style.transition = "transform 0.5s ease";
    track.style.transform = `translateY(-${index * 180}px)`;
}

setInterval(moverCarrusel, 3000);


// mensajes
function mostrarMensajeTestimonio(texto, tipo="error") {
    const mensaje = document.getElementById("mensaje-testimonio");

    mensaje.classList.remove("show");

    setTimeout(() => {
        mensaje.textContent = texto;
        mensaje.className = "mensaje show " + tipo;
    }, 100);

    setTimeout(() => {
        mensaje.classList.remove("show");
    }, 4000);
}