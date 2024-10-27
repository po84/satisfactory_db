    // Add Todo JS
    const newComponentForm = document.getElementById('newComponentForm');
    if (newComponentForm) {
        newComponentForm.addEventListener('submit', async function (event) {
            event.preventDefault();

            const form = event.target;
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());

            const payload = {
                name: data.name,
                is_raw_material: data.is_raw_material === "on",
                tier: parseInt(data.tier),
            };

            try {
                const response = await fetch('/components', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(payload)
                });

                if (response.ok) {
                    form.reset(); // Clear the form
                } else {
                    // Handle error
                    const errorData = await response.json();
                    alert(`Error: ${errorData.detail}`);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            }
        });
    }

    // Edit Todo JS
    const editComponentForm = document.getElementById('editComponentForm');
    if (editComponentForm) {
        editComponentForm.addEventListener('submit', async function (event) {
        event.preventDefault();
        const form = event.target;
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        var url = window.location.pathname;
        const componentId = url.substring(url.lastIndexOf('/') + 1);

        const payload = {
            name: data.name,
            is_raw_material: data.is_raw_material === "on",
            tier: parseInt(data.tier),
        };

        try {
            const response = await fetch(`/components/${componentId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                window.location.href = '/components-page'; // Redirect to the components page
            } else {
                // Handle error
                const errorData = await response.json();
                alert(`Error: ${errorData.detail}`);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        }
    });

        document.getElementById('deleteButton').addEventListener('click', async function () {
            var url = window.location.pathname;
            const todoId = url.substring(url.lastIndexOf('/') + 1);

            try {
                const response = await fetch(`/components/${todoId}`, {
                    method: 'DELETE',
                });

                if (response.ok) {
                    // Handle success
                    window.location.href = '/components-page'; // Redirect to the components page
                } else {
                    // Handle error
                    const errorData = await response.json();
                    alert(`Error: ${errorData.detail}`);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            }
        });

        
    }
