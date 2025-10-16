document.getElementById("chat-form").addEventListener("submit", async function (e) {
    e.preventDefault();

    // Obtener valores del formulario
    const modelo = document.getElementById("modelo").value;
    const pregunta = document.getElementById("pregunta").value;

    // Validar que la pregunta no esté vacía
    if (!pregunta.trim()) {
        alert("Por favor, escribe tu pregunta");
        return;
    }

    // Mostrar "cargando" mientras se espera la respuesta
    document.getElementById("response").style.display = "block";
    document.getElementById("respuesta").innerHTML = `
        <div class="d-flex align-items-center">
            <div class="spinner-border text-primary me-3" role="status"></div>
            <div>Analizando tu pregunta con nuestros expertos...</div>
        </div>
    `;

    // Realizar la solicitud a la API
    try {
        const response = await fetch('http://127.0.0.1:8000/preguntar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                modelo: modelo,
                pregunta: pregunta
            })
        });

        const data = await response.json();

        // Mostrar la respuesta de la API
        document.getElementById("respuesta").innerHTML = `
            <div class="mb-2"><strong>Modelo consultado:</strong> ${modelo}</div>
            <div><strong>Tu pregunta:</strong> ${pregunta}</div>
            <div class="mt-3 alert alert-info bg-primary bg-opacity-10 border-primary">
                <i class="fas fa-info-circle me-2"></i> ${data.respuesta || "No se encontró una respuesta específica. Por favor, reformula tu pregunta."}
            </div>
            <div class="mt-3 text-center">
                <button class="btn btn-sm btn-outline-primary" onclick="document.getElementById('pregunta').value = ''; document.getElementById('pregunta').focus()">
                    <i class="fas fa-plus me-1"></i> Hacer otra pregunta
                </button>
            </div>
        `;
    } catch (error) {
        document.getElementById("respuesta").innerHTML = `
            <div class="alert alert-danger">
                <i class="fas fa-exclamation-triangle me-2"></i> Hubo un error al procesar tu solicitud. Por favor, inténtalo de nuevo.
            </div>
        `;
    }
});

// Manejar preguntas frecuentes
document.querySelectorAll('.question-tag').forEach(tag => {
    tag.addEventListener('click', function() {
        document.getElementById('pregunta').value = this.getAttribute('data-question');
        document.getElementById('pregunta').focus();
    });
});