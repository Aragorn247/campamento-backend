document.addEventListener('DOMContentLoaded', () => {
    const loginSection = document.getElementById('login-section');
    const dashboardSection = document.getElementById('dashboard-section');
    const loginForm = document.getElementById('loginForm');
    const logoutBtn = document.getElementById('logoutBtn');
    const messageDiv = document.getElementById('message');

    // 1. Validar si ya existe una sesión activa al cargar la página
    if (localStorage.getItem('jwt_token')) {
        showDashboard();
    }

    // 2. Manejador del formulario de Login
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const emailInput = document.getElementById('username').value;
        const passwordInput = document.getElementById('password').value;

        messageDiv.className = '';
        messageDiv.textContent = 'Autenticando...';

        try {
            const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    email: emailInput,
                    password: passwordInput
                })
            });

            const data = await response.json();

            if (response.ok) {
                localStorage.setItem('jwt_token', data.access_token);
                
                messageDiv.className = 'success';
                messageDiv.textContent = '¡Login exitoso! Token guardado.';

                // Transición fluida al panel de actividades
                setTimeout(() => {
                    showDashboard();
                }, 800);
            } else {
                messageDiv.className = 'error';
                messageDiv.textContent = data.message || data.msg || 'Usuario o contraseña incorrectos.';
            }
        } catch (error) {
            console.error('Error de conexión:', error);
            messageDiv.className = 'error';
            messageDiv.textContent = 'Error al conectar con el servidor backend.';
        }
    });

    // 3. Manejador de Cierre de Sesión
    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            localStorage.removeItem('jwt_token');
            dashboardSection.classList.add('hidden');
            loginSection.classList.remove('hidden');
            loginForm.reset();
            messageDiv.textContent = '';
        });
    }

    // Función para alternar vistas y disparar la carga de datos
    async function showDashboard() {
        if (loginSection && dashboardSection) {
            loginSection.classList.add('hidden');
            dashboardSection.classList.remove('hidden');
        }
        await loadActivities();
    }

    // 4. Petición protegida GET para obtener el listado de actividades
    async function loadActivities() {
        const token = localStorage.getItem('jwt_token');
        const container = document.getElementById('activities-list');
        
        if (!container) return;
        container.innerHTML = '<p>Cargando actividades...</p>';

        try {
            const response = await fetch('http://127.0.0.1:5000/api/v1/activities', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                }
            });

            const data = await response.json();

            if (response.ok) {
                renderActivities(data);
            } else {
                container.innerHTML = '<p class="error">Error al cargar las actividades del campamento.</p>';
                if (response.status === 401) {
                    localStorage.removeItem('jwt_token');
                    dashboardSection.classList.add('hidden');
                    loginSection.classList.remove('hidden');
                }
            }
        } catch (error) {
            console.error('Error de red:', error);
            container.innerHTML = '<p class="error">No se pudo conectar con el servidor de actividades.</p>';
        }
    }

    // 5. Renderizado dinámico de las tarjetas de actividades con botón de reserva
    function renderActivities(activities) {
        const container = document.getElementById('activities-list');
        container.innerHTML = '';

        if (!activities || activities.length === 0) {
            container.innerHTML = '<p>No hay actividades registradas actualmente.</p>';
            return;
        }

        activities.forEach(activity => {
            const card = document.createElement('div');
            card.className = 'activity-card';
            
            // Usamos un ID seguro (compatible con id o _id según devuelva la API)
            const activityId = activity.id || activity._id;

            card.innerHTML = `
                <h4 style="margin: 0 0 5px 0; color: #333;">${activity.name || activity.title || 'Actividad'}</h4>
                <p style="margin: 0 0 5px 0; font-size: 14px; color: #555;">${activity.description || 'Sin descripción'}</p>
                <p style="margin: 0 0 10px 0; font-size: 13px; color: #777;"><strong>Plazas:</strong> ${activity.capacity ?? 'N/D'}</p>
                <button type="button" class="btn-book" data-id="${activityId}" style="padding: 6px 12px; font-size: 14px; background-color: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer;">Reservar Plaza</button>
            `;
            container.appendChild(card);
        });

        // Adjuntar eventos a los botones de reserva generados
        document.querySelectorAll('.btn-book').forEach(button => {
            button.addEventListener('click', async (e) => {
                const activityId = e.target.getAttribute('data-id');
                await bookActivity(activityId);
            });
        });
    }

    // 6. Petición protegida POST para reservar una actividad
    async function bookActivity(activityId) {
        const token = localStorage.getItem('jwt_token');

        try {
            const response = await fetch(`http://127.0.0.1:5000/api/v1/activities/${activityId}/book`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                }
            });

            const data = await response.json();

            if (response.ok) {
                alert('¡Reserva realizada con éxito!');
                loadActivities(); // Recargar el listado para reflejar cambios en plazas si aplica
            } else {
                alert(data.message || data.msg || 'No se pudo completar la reserva.');
            }
        } catch (error) {
            console.error('Error al reservar:', error);
            alert('Error de conexión al intentar reservar la actividad.');
        }
    }
});