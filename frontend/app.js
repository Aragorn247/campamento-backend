document.addEventListener('DOMContentLoaded', () => {
    const loginSection = document.getElementById('login-section');
    const dashboardSection = document.getElementById('dashboard-section');
    const loginForm = document.getElementById('loginForm');
    const logoutBtn = document.getElementById('logoutBtn');
    const messageDiv = document.getElementById('message');
    const createActivityForm = document.getElementById('createActivityForm');
    const adminMessage = document.getElementById('admin-message');

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
            if (createActivityForm) createActivityForm.reset();
            if (adminMessage) adminMessage.textContent = '';
        });
    }

    // Función para alternar vistas y disparar la carga de datos
    async function showDashboard() {
        if (loginSection && dashboardSection) {
            loginSection.classList.add('hidden');
            dashboardSection.classList.remove('hidden');
        }
        await loadActivities();
        await loadMyBookings();
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
                    handleUnauthorized();
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
            const activityId = activity.id || activity._id;

            card.innerHTML = `
                <h4 style="margin: 0 0 5px 0; color: #333;">${activity.name || activity.title || 'Actividad'}</h4>
                <p style="margin: 0 0 5px 0; font-size: 14px; color: #555;">${activity.description || 'Sin descripción'}</p>
                <p style="margin: 0 0 10px 0; font-size: 13px; color: #777;"><strong>Plazas:</strong> ${activity.capacity ?? 'N/D'}</p>
                <button type="button" class="btn-book" data-id="${activityId}" style="padding: 6px 12px; font-size: 14px; background-color: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer;">Reservar Plaza</button>
            `;
            container.appendChild(card);
        });

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
            const response = await fetch('http://127.0.0.1:5000/api/v1/bookings', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    activity_id: parseInt(activityId)
                })
            });

            const data = await response.json();

            if (response.ok) {
                alert('¡Reserva realizada con éxito!');
                loadActivities();
                loadMyBookings();
            } else {
                alert(data.message || data.msg || 'No se pudo completar la reserva.');
            }
        } catch (error) {
            console.error('Error al reservar:', error);
            alert('Error de conexión al intentar reservar la actividad.');
        }
    }

    // 7. Petición protegida GET para obtener las reservas del usuario
    async function loadMyBookings() {
        const token = localStorage.getItem('jwt_token');
        const container = document.getElementById('my-bookings-list');

        if (!container) return;
        container.innerHTML = '<p>Cargando tus reservas...</p>';

        try {
            const response = await fetch('http://127.0.0.1:5000/api/v1/bookings/my-bookings', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                }
            });

            const data = await response.json();

            if (response.ok) {
                renderMyBookings(data);
            } else {
                container.innerHTML = '<p class="error">Error al cargar tus reservas.</p>';
                if (response.status === 401) {
                    handleUnauthorized();
                }
            }
        } catch (error) {
            console.error('Error de red:', error);
            container.innerHTML = '<p class="error">No se pudo conectar con el servidor de reservas.</p>';
        }
    }

    // 8. Renderizado dinámico de las reservas del usuario
    function renderMyBookings(bookings) {
        const container = document.getElementById('my-bookings-list');
        container.innerHTML = '';

        if (!bookings || bookings.length === 0) {
            container.innerHTML = '<p style="font-size: 14px; color: #666;">No tienes reservas activas actualmente.</p>';
            return;
        }

        bookings.forEach(booking => {
            const card = document.createElement('div');
            card.className = 'activity-card';
            card.style.backgroundColor = '#eef9ff';
            
            const activityName = booking.activity_name || booking.activity?.name || `Actividad #${booking.activity_id}`;
            const bookingDate = booking.created_at ? new Date(booking.created_at).toLocaleDateString() : '';

            card.innerHTML = `
                <h4 style="margin: 0 0 5px 0; color: #0056b3;">${activityName}</h4>
                <p style="margin: 0; font-size: 13px; color: #555;">${bookingDate ? `Reservado el: ${bookingDate}` : 'Reserva confirmada'}</p>
            `;
            container.appendChild(card);
        });
    }

    // 9. Manejador para la creación de nuevas actividades (Admin)
    if (createActivityForm) {
        createActivityForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const token = localStorage.getItem('jwt_token');

            const name = document.getElementById('actName').value;
            const description = document.getElementById('actDesc').value;
            const capacity = parseInt(document.getElementById('actCapacity').value);
            const price = parseFloat(document.getElementById('actPrice').value);

            adminMessage.className = '';
            adminMessage.textContent = 'Creando actividad...';

            try {
                const response = await fetch('http://127.0.0.1:5000/api/v1/activities', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({
                        name,
                        description,
                        capacity,
                        price
                    })
                });

                const data = await response.json();

                if (response.ok) {
                    adminMessage.className = 'success';
                    adminMessage.style.color = 'green';
                    adminMessage.textContent = '¡Actividad creada exitosamente!';
                    createActivityForm.reset();
                    loadActivities(); // Recargar el listado general
                } else {
                    adminMessage.className = 'error';
                    adminMessage.style.color = 'red';
                    adminMessage.textContent = data.message || data.msg || 'No se pudo crear la actividad.';
                }
            } catch (error) {
                console.error('Error al crear actividad:', error);
                adminMessage.className = 'error';
                adminMessage.style.color = 'red';
                adminMessage.textContent = 'Error de conexión con el servidor.';
            }
        });
    }

    // Función auxiliar para manejar tokens no válidos o expirados
    function handleUnauthorized() {
        localStorage.removeItem('jwt_token');
        dashboardSection.classList.add('hidden');
        loginSection.classList.remove('hidden');
    }
});