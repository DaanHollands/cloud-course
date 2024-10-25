---
title: "REST api in laravel"
weight: 7
author: Arne Duyver
draft: false
---
## 6: Demo 3
Verder kunnen we onze laravel website uitbreiden met een eigen REST API gedefinieerd in laravel zelf (of in een andere laravel applicatie die op een andere server draait)

Hiervoor maken we dan wel een LaravelUser model aan omdat we nu effectief de laravel database gaan gebruiken: `php artisan make:model LaravelUser -mcf`. Met dit commando wordt er ook automatisch een migrationTable en Controller aangemaakt.

In de controller gaan we nu dan de functionaliteit van onze REST API programmeren volledig analoog aan onze Flask implementatie alleen moeten we nu PHP specifieke syntax gebruiken:
<details open>
    <summary><i><b>Klik hier om de code te zien/verbergen voor `app/Http/LaravelUserController.php`</b></i></summary>
    <p>

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use App\Models\LaravelUser;

class LaravelUserController extends Controller
{
    // Get all laravelUsers
    public function getLaravelUsers(Request $request)
    {
        $pwd = $request->query('pwd');
        if ($pwd == 'mypassword') {
            $laravelUsers = LaravelUser::all();
            return response()->json($laravelUsers, 200);
        } else {
            return response()->json(['message' => 'Wrong password mate'], 403);
        }
    }

    // Get a single laravelUser by ID
    public function getLaravelUser($id)
    {
        $laravelUser = LaravelUser::find($id);
        if ($laravelUser) {
            return response()->json($laravelUser, 200);
        } else {
            return response()->json(['message' => 'User not found'], 404);
        }
    }

    // Create a new laravelUser
    public function createLaravelUser(Request $request)
    {
        $name = $request->input('name');
        $email = $request->input('email');

        if (!$name || !$email) {
            return response()->json(['error' => 'Name and email required'], 400);
        }

        try {
            $laravelUser = new LaravelUser();
            $laravelUser->name = $name;
            $laravelUser->email = $email;
            $laravelUser->save();

            return response()->json(['message' => 'User created successfully'], 201);
        } catch (\Exception $e) {
            return response()->json(['error' => $e->getMessage()], 500);
        }
    }

    // Delete a laravelUser
    public function deleteLaravelUser($id)
    {
        $laravelUser = LaravelUser::find($id);
        if (!$laravelUser) {
            return response()->json(['message' => 'User not found'], 404);
        }

        $laravelUser->delete();
        return response()->json(['message' => 'User deleted successfully'], 200);
    }
}
```
</p>
</details>

Ook het LaravelUser model moet nu correct zijn en bijhorende migration table om de objecten correct op te slaan in de database:
### model: `app/Models/LaravelUser.php`

<details open>
    <summary><i><b>Klik hier om de code te zien/verbergen voor `app/Models/LaravelUser.php``</b></i></summary>
    <p>

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class LaravelUser extends Model
{
    use HasFactory;

    // Specify the table name if it's not the plural of the model name
    protected $table = 'laravelUsers';

    // The attributes that are mass assignable
    protected $fillable = [
        'name',
        'email',
    ];

    // Disable timestamps if your table doesn't have created_at and updated_at columns
    public $timestamps = true;
}
```
</p>
</details>

### migration `database/migrations/2024_10_14_074850_create_laravel_users_table.php`
<details open>
    <summary><i><b>Klik hier om de code te zien/verbergen voor `database/migrations/2024_10_14_074850_create_laravel_users_table.php`</b></i></summary>
    <p>

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up()
    {
        Schema::create('laravelUsers', function (Blueprint $table) {
            $table->id();
            $table->string('name');
            $table->string('email')->unique();
            $table->timestamps();
        });
    }



    /**
     * Reverse the migrations.
     */
    public function down()
    {
        Schema::dropIfExists('laravelUsers');
    }
};

```

</p>
</details>

### Routes: api.php
Ten slotte moeten we onze routes nog definiëren in een nieuwe file `routes/api.php`. Op die manier kunnen we de endpoints bereiken via `www.mijnlaravelwebsite.com/api/...`

De file ziet er als volgt uit:

<details open>
    <summary><i><b>Klik hier om de code te zien/verbergen voor `routes/api.php`</b></i></summary>
    <p>

```php
<?php

use App\Http\Controllers\LaravelUserController;

Route::get('/laravelUsers', [LaravelUserController::class, 'getLaravelUsers']);
Route::get('/laravelUsers/{id}', [LaravelUserController::class, 'getLaravelUser']);
Route::post('/laravelUsers', [LaravelUserController::class, 'createLaravelUser']);
Route::delete('/laravelUsers/{id}', [LaravelUserController::class, 'deleteLaravelUser']);
```
</p>
</details>

We kunnen nu dan ook een de users view in ons hoofdproject aanpassen en deze endpoints gebruiken in plaats van de Flask endpoints: `views/users.blade.php`

<details open>
    <summary><i><b>Klik hier om de code te zien/verbergen voor `views/users.blade.php`</b></i></summary>
    <p>

```php
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Laravel Users</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
<div class="container">
    <h1 class="my-4">Laravel Users</h1>

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
        fetch('/api/laravelUsers?pwd=mypassword')
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
        fetch(`/api/laravelUsers/${id}`, {
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

        fetch('/api/laravelUsers', {
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

**Een laatste belangrijke aanpassing die we moeten maken is aan het Laravel project laten weten dat we extra api endpoint hebben toegevoegd.** Dit doe je door de file `app/Providers/AppServiceProvider.php` aan te passen:


<details open>
    <summary><i><b>Klik hier om de code te zien/verbergen voor `app/Providers/AppServiceProvider.php`</b></i></summary>
    <p>

```php
<?php

namespace App\Providers;


use Illuminate\Support\Facades\Route;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        //
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Route::middleware('api')
            ->prefix('api')
            ->group(base_path('routes/api.php'));
    }
}
```


</p>
</details>


## Factory and Seeders
Je kan Laravel nu ook gebruiken om automatisch wat dummy data te genereren in de database. Hierover vind je meer op volgende website: [FSWEB](https://kuleuven-diepenbeek.github.io/fsweb-course/backend/laravel_code/) of via deze [video](https://www.youtube.com/watch?v=YETNihHReo4)


## Enable CORS

1. Voeg volgende module toe aan het project: `composer require fruitcake/laravel-cors`
2. Pas volgende file aan of maak hem aan als hij nog niet bestaat: `config/cors.php`
<details open>
    <summary><i><b>Klik hier om de code te zien/verbergen voor `config/cors.php`</b></i></summary>
    <p>

```php
<?php

return [

    /*
    |--------------------------------------------------------------------------
    | Laravel CORS Configuration
    |--------------------------------------------------------------------------
    |
    | Here you may configure your settings for cross-origin resource sharing
    | or "CORS". This determines what cross-origin operations may execute
    | in web browsers. You are free to adjust these settings as needed.
    |
    | To learn more: https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS
    |
    */

    'paths' => ['api/*'],  // Geeft aan voor welke routes CORS ingeschakeld moet worden

    'allowed_methods' => ['*'], // Toegestane HTTP-methoden zoals GET, POST, PUT, DELETE. '*' staat voor alle methoden

    'allowed_origins' => ['*'], // Toegestane origins. '*' betekent dat elke origin is toegestaan

    'allowed_origins_patterns' => [], // Regex-patronen voor meer specifieke origin matching

    'allowed_headers' => ['*'], // Headers die zijn toegestaan in CORS-verzoeken

    'exposed_headers' => [], // Headers die zichtbaar zijn in de client (bijvoorbeeld 'Authorization')

    'max_age' => 0, // Hoe lang de resultaten van een preflight request worden gecached (in seconden)

    'supports_credentials' => false, // Als je cookies of authorization headers toestaat, zet deze op true

];

```

</p>
</details>

3. Controleer of de CORS-middleware is geregistreerd in de kernel. Open het bestand `app/Http/Kernel.php` en controleer of de CORS-middleware aanwezig is in de api middleware-groep.

<details open>
    <summary><i><b>Klik hier om de code te zien/verbergen voor `app/Http/Kernel.php`</b></i></summary>
    <p>

```php
protected $middlewareGroups = [
    'api' => [
        \Illuminate\Routing\Middleware\SubstituteBindings::class,
        \Fruitcake\Cors\HandleCors::class, // Zorg dat deze regel aanwezig is
    ],
];
```

</p>
</details>

4. Verwijder de cache van configuratiebestanden: `php artisan config:clear`