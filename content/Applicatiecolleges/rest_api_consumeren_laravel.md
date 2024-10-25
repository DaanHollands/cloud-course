---
title: "REST api consumeren in laravel"
weight: 6
author: Arne Duyver
draft: false
---

# REST api oproepen in Laravel vanuit de frontend met Javascript
## 6: Demo 1
Om een ​​Laravel-project te maken dat communiceert met de REST API met behulp van JavaScript in de frontend, moeten we volgende zaken doen:

1. Laravel project aanmaken
2. Gebruik JavaScript om de Flask API aan te roepen
3. Creëer de nodige Laravel controllers
4. Configureer routes

## Laravel project aanmaken
```bash
composer create-project laravel/laravel consumeApi
# change database type to 'mysql' in .env
cd /consumeApi
php artisan migrate
# start onze website, host 0.0.0.0 is nodig om correct met docker te werken
php artisan serve --host 0.0.0.0
```

## Laravel views en Javascript calls
We gebruiken JavaScript (met fetch) om de Flask REST API op te roepen.
Maak een nieuwe lay-out als deze niet bestaat en voeg vervolgens de benodigde HTML-structuure: `views/users.blade.php`
<details open>
    <summary><i><b>Klik hier om de code te zien/verbergen voor `views/users.blade.php`</b></i></summary>
    <p>

```php
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Laravel + Flask API Integration</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.1.3/css/bootstrap.min.css">
</head>
<body>
    <div class="container mt-5">
    <h1>User List</h1>
    <ul class="list-group" id="users-list">
        <!-- Users will be populated here by JavaScript -->
    </ul>

    <!-- Input field so new users can be created or old ones updated -->
    <hr>
    <h2>Add User</h2>
    <form id="add-user-form" onsubmit="addUser(event)">
        <div class="mb-3">
            <label for="name" class="form-label">Name</label>
            <input type="text" class="form-control" id="name" required>
        </div>
        <div class="mb-3">
            <label for="email" class="form-label">Email</label>
            <input type="email" class="form-control" id="email" required>
        </div>
        <button type="submit" class="btn btn-primary">Add User</button>
    </form>
    </div>

    <script>
        // Voer de functie fetchUsers uit wanneer deze pagina geladen wordt.
        window.onload = fetchUsers;

        // HTTP GET request
        // async want we willen niet dat onze website blijft hangen totdat je antwoord hebt gekregen van de API
        async function fetchUsers() {
            try {
                // AWAIT, wacht dus totdat de fetch iets heeft teruggeven en steek dit dan in de variabele respons
                // De fetch functie gebruikt standaard GET requests
                let response = await fetch(`http://localhost:5000/api/users?pwd=mypassword`);
                // response bevat meer informatie, maar we zijn eigenlijk enkel geinteresseerd in de data die we terugkrijgen in JSON formaat
                let data = await response.json();
                // Maak nu mooie html code aan om elke gebruiker te tonen
                displayUsers(data);
            } catch (error) {
                console.error('Error fetching users:', error);
            }
        }

        // Maak mooie html code aan om elke gebruiker te tonen
        function displayUsers(users) {
            let usersList = document.getElementById('users-list');
            // delete alle inhoud van het HTML element met id 'users-list'
            usersList.innerHTML = '';

            // maak een HTML blokje aan voor elke gebruiker (met naam, email en een delete knop) en voeg die toe aan de users-list
            users.forEach(user => {
                let listItem = `<li class="list-group-item">
                    ${user.name} - ${user.email}
                    <button class="btn btn-danger btn-sm float-end" onclick="deleteUser(${user.id})">Delete</button>
                </li>`;
                usersList.innerHTML += listItem;
            });
        }
        
        // De code die uitgevoerd moet worden wanneer op de delete knop gedrukt wordt
        async function deleteUser(userId) {
            try {
                // Specifieer dat we een DELETE HTTP request willen sturen
                let response = await fetch(`http://localhost:5000/api/users/${userId}`, {
                    method: 'DELETE'
                });
                if (response.ok) {
                    alert('User deleted successfully');
                    fetchUsers();  // Refresh list
                }
            } catch (error) {
                console.error('Error deleting user:', error);
            }
        }

        // De code die uitgevoerd moet worden om een nieuwe gebruiker aan te maken
        async function addUser(event) {
            //Zorgt ervoor dat dit event niet zomaar getriggerd wordt
            event.preventDefault();
            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;

            try {
                // We specifieren in de HEADER op welke manier de data in de BODY gecodeerd is. Het JSON object steken we dan in de body
                let response = await fetch("http://localhost:5000/api/users", {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ name: name, email: email })
                });

                if (response.ok) {
                    alert('User added successfully');
                    document.getElementById('add-user-form').reset();
                    fetchUsers();  // Refresh user list
                } else {
                    alert('Error adding user');
                }
            } catch (error) {
                console.error('Error adding user:', error);
            }
        }
    </script>
</body>
</html>
```
</p>
</details>

## Routes definiëren

Definieer in `routes/web.php` een route om de users view te laden.

```php
use Illuminate\Support\Facades\Route;

Route::get('/users', function () {
    return view('users');
});
```

Open nu de Laravel-frontend (http://localhost:8000/users) en je zou de users view moeten zien, samen met het formulier om users toe te voegen. CRUD-bewerkingen zoals "Toevoegen" en "Verwijderen" worden uitgevoerd via JavaScript-calls naar de Flask API. 
Zorg ervoor dat je Flask applicatie aan het runnen is.


## Opdracht:
Voeg een geslacht toe aan de gebruikers en pas alle nodige code aan in de Flask applicatie en de Laravel applicatie.

# REST api oproepen in Laravel vanuit de backend met php (flask app en laravel in 1 docker-compose file)
## 6: Demo 2
We kunnen een extra route toevoegen in de `routes/web.php` naar `/usersBackend`. We maken hier weer een nieuwe view voor aan. De functionaliteit van het endpoint kunnen we volledig definiëren in `web.php`. Om met de requests te kunnen werken hebben we de Guzzle module nodig. Installeer deze via `composer require guzzlehttp/guzzle`

We kunnen nu gelijkaardige HTML code gebruiken als bovenstaande, maar de javascript kan nu grotendeels weggelaten worden: `views/usersBackend.blade.php`. De view gaat nu van php automatisch een list van users meekrijgen, die we kunnen uilezen in blade.php files met: `$users`

<details open>
    <summary><i><b>Klik hier om de code te zien/verbergen voor `views/usersBackend.blade.php`</b></i></summary>
    <p>

```php
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Laravel + Flask API Integration backend</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.1.3/css/bootstrap.min.css">
</head>
<body>
    <div class="container mt-5">
    <h1>User List</h1>
    <ul class="list-group" id="users-list">
        @foreach ($users as $user)
        <li class="list-group-item">
            {{ $user->name }} - {{ $user->email }}
        </li>
        @endforeach
    </ul>
    </div>
</body>
</html>
```

</p>
</details>


Nu kunnen we volgende functionaliteit implementeren in de `web.php`

<details open>
    <summary><i><b>Klik hier om de code te zien/verbergen voor `routes/web.php`</b></i></summary>
    <p>

```php
// Vergeet de modules Request en Guzzle/Client niet te importeren
use Illuminate\Http\Request;
use GuzzleHttp\Client;

// ...

Route::get('/usersBackend', function () {
    // Maak een HTTP-verzoek naar de Flask API
    // uri is de flask service uit onze docker-compose
    $client = new Client(['base_uri' => 'server2:5000']);
    // GET alle users op endpoint /api/users met als parameter pwd=mypassword
    $response = $client->get('/api/users', [
        'query' => ['pwd' => 'mypassword']
    ]);
    $users = json_decode($response->getBody()->getContents(), true);   
    // Stuur de lijst van gebruikers naar de view
    return view('usersBackend', ['users' => $users]);
});
    
```

</p>
</details>

## Models, controllers
Willen we nu echter meer functionaliteit dan kunnen we best eigen endpoints in Laravel definiëren die op hun beurt een oproep gaan doen naar de Flask API. We laten onze frontend dan onze Laravel endpoints aanroepen om via de backend de call naar de Flask API uit te voeren. Hiervoor kunnen we best een Controller aanmaken die de calls doet naar de API. 

Je kan een controller aanmaken via `php artisan make:controller FlaskUserController`. Het bestand bevindt zich nu in `app/Http/Controllers/FlaskUserController.php` en laten we er als volgend uitzien:
<details open>
    <summary><i><b>Klik hier om de code te zien/verbergen voor `app/Http/Controllers/FlaskUserController.php`</b></i></summary>
    <p>

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use GuzzleHttp\Client;

class FlaskUserController extends Controller
{
    // Definieer een Client object dat we binnen de controller kunnen herbruiken
    protected $client;

    public function __construct()
    {
        // uri is de flask service uit onze docker-compose
        $this->client = new Client(['base_uri' => 'server2:5000']);
    }

    // GET all users
    public function index(Request $request)
    {
        $response = $this->client->get('/api/users', [
            'query' => ['pwd' => 'mypassword']
        ]);

        $users = json_decode($response->getBody()->getContents(), true);
        return response()->json($users);
    }

    // GET single user
    public function show($id)
    {
        try {
            $response = $this->client->get("/api/users/{$id}");
            $user = json_decode($response->getBody()->getContents(), true);

            return response()->json($user);
        } catch (\Exception $e) {
            return response()->json(['error' => 'User not found'], 404);
        }
    }

    // POST create user
    public function store(Request $request)
    {
        $data = [
            'name' => $request->input('name'),
            'email' => $request->input('email'),
        ];

        try {
            $response = $this->client->post('/api/users', [
                'json' => $data
            ]);

            return response()->json(json_decode($response->getBody(), true), $response->getStatusCode());
        } catch (\Exception $e) {
            return response()->json(['error' => $e->getMessage()], 500);
        }
    }

    // DELETE user
    public function destroy($id)
    {
        try {
            $response = $this->client->delete("/api/users/{$id}");

            return response()->json(json_decode($response->getBody(), true), $response->getStatusCode());
        } catch (\Exception $e) {
            return response()->json(['error' => $e->getMessage()], 500);
        }
    }
}
```

</p>
</details>

We voegen de import van onze FlaskUserController toe aan de `web.php` en definiëren de verschillende endpoints:

<details open>
    <summary><i><b>Klik hier om de code te zien/verbergen voor `routes/web.php`</b></i></summary>
    <p>

```php
use App\Http\Controllers\FlaskUserController;

Route::get('/users',function () {
    return view('users');
});

Route::get('/flaskusers', [FlaskUserController::class, 'index']);
Route::get('/users/{id}', [FlaskUserController::class, 'show']);
Route::post('/users', [FlaskUserController::class, 'store']);
Route::delete('/users/{id}', [FlaskUserController::class, 'destroy']);
```
</p>
</details>

Nu moeten we onze `views/users.blade.php` nog aanpassen zodat de fetch gebeurt naar de lokale endpoints.

<details open>
    <summary><i><b>Klik hier om de code te zien/verbergen voor `views/users.blade.php`</b></i></summary>
    <p>

```php
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask Users</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
<div class="container">
    <h1 class="my-4">Flask Users</h1>

    <!-- Display Users -->
    <h2>All Users</h2>
    <table class="table table-striped" id="usersTable">
        <thead>
        <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Actions</th>
        </tr>
        </thead>
        <tbody>
        </tbody>
    </table>

    <!-- Add New User -->
    <h2>Add New User</h2>
    <form id="createUserForm">
        <div class="mb-3">
            <label for="name" class="form-label">Name</label>
            <input type="text" class="form-control" id="name" name="name" required>
        </div>
        <div class="mb-3">
            <label for="email" class="form-label">Email</label>
            <input type="email" class="form-control" id="email" name="email" required>
        </div>
        <button type="submit" class="btn btn-primary">Create User</button>
    </form>

    <!-- Error or Success Messages -->
    <div id="message" class="mt-4"></div>
</div>

<script>
    // Function to fetch users and populate the table
    function fetchUsers() {
        // Hier doen we dus een oproep naar het lokale endpoint
        fetch('/flaskusers')
            .then(response => response.json())
            .then(users => {
                const usersTable = document.getElementById('usersTable').getElementsByTagName('tbody')[0];
                usersTable.innerHTML = '';  // Clear existing rows

                users.forEach(user => {
                    const row = usersTable.insertRow();
                    row.insertCell(0).textContent = user.id;
                    row.insertCell(1).textContent = user.name;
                    row.insertCell(2).textContent = user.email;

                    const actionsCell = row.insertCell(3);
                    const deleteButton = document.createElement('button');
                    deleteButton.textContent = 'Delete';
                    deleteButton.className = 'btn btn-danger btn-sm';
                    deleteButton.onclick = () => deleteUser(user.id);
                    actionsCell.appendChild(deleteButton);
                });
            })
            .catch(error => console.error('Error fetching users:', error));
    }

    // Function to delete a user
    function deleteUser(id) {
        fetch(`/users/${id}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('message').innerHTML = `<div class="alert alert-success">${data.message}</div>`;
            fetchUsers();  // Refresh the user list
        })
        .catch(error => {
            console.error('Error deleting user:', error);
            document.getElementById('message').innerHTML = `<div class="alert alert-danger">Failed to delete user</div>`;
        });
    }

    // Handle form submission for creating a new user
    document.getElementById('createUserForm').addEventListener('submit', function (event) {
        event.preventDefault();

        const formData = {
            name: document.getElementById('name').value,
            email: document.getElementById('email').value,
        };

        fetch('/users', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('message').innerHTML = `<div class="alert alert-success">${data.message}</div>`;
            document.getElementById('createUserForm').reset();  // Clear form
            fetchUsers();  // Refresh the user list
        })
        .catch(error => {
            console.error('Error creating user:', error);
            document.getElementById('message').innerHTML = `<div class="alert alert-danger">Failed to create user</div>`;
        });
    });

    // Fetch users on page load
    fetchUsers();
</script>
</body>
</html>
```

</p>
</details>

