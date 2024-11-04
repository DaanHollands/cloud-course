---
title: "GraphQL api consumeren in laravel"
weight: 9
author: Arne Duyver
draft: false
---

## Wat is GraphQL?

GraphQL is een querytaal voor APIs en een runtime voor het uitvoeren van die queries. GraphQL biedt een efficiënter, krachtiger en flexibeler alternatief voor REST APIs. Met GraphQL kunnen clients precies de gegevens opvragen die ze nodig hebben, waardoor het overvragen of ondervragen van data wordt voorkomen.

## Werking

GraphQL werkt via één enkel endpoint (meestal `/graphql`) en gebruikt een schema om de beschikbare datatypes en hun onderlinge relaties te definiëren. Het schema bestaat uit:

- **Types**: Definities van objecten, velden en hun relaties.
- **Queries**: Verzoeken om data op te halen.
- **Mutations**: Verzoeken om data aan te passen.
- **Subscriptions**: Realtime data-updates.

Een GraphQL-query lijkt op de vorm van de JSON-response die het zal returnen. Clients specificeren precies welke velden ze nodig hebben, en de server haalt alleen die velden op, wat zorgt voor efficiëntie.

### Belangrijke Componenten

1. **Schema**: Definieert de beschikbare datatypes en queries in de API.
2. **Resolvers**: Functies die aangeven hoe de data voor elk veld in het schema opgehaald moet worden.
3. **Uitvoering van Query's**: De client stuurt een query, en de GraphQL-runtime vergelijkt de query met het schema en voert deze uit via de resolvers.

Voorbeeld van een GraphQL-query:
```graphql
query {
  user(id: "1") {
    name
    email
    posts {
      title
    }
  }
}
```

De bovenstaande query vraagt de `name` en `email` van een gebruiker, samen met de bijbehorende `posts`, maar alleen de `title` van elke post.

## Voordelen van GraphQL

- **Efficiënt Data ophalen**: Clients vragen alleen de specifieke data op die ze nodig hebben, wat under- en overfetching minimaliseert en zo de netwerkbelasting vermindert.
- **Enkel endpoint**: In tegenstelling tot REST, dat vaak meerdere eindpunten vereist, gebruikt GraphQL één endpoint voor alle verzoeken, wat het API-beheer vereenvoudigt.
- **Sterk Getypeerd Schema**: Een goed gedefinieerd schema functioneert als een contract tussen client en server, wat het eenvoudiger maakt om data te begrijpen en te valideren.
- **Geen Versies Nodig**: Met GraphQL kunnen nieuwe velden aan het schema worden toegevoegd zonder bestaande clients te beïnvloeden, waardoor de noodzaak voor versiebeheer afneemt.
- **Realtime Data met Subscriptions**: GraphQL ondersteunt realtime-updates via subscriptions, ideaal voor applicaties die live data-updates nodig hebben.
- **Ontwikkelaarservaring**: Tools zoals GraphiQL of GraphQL Playground laten ontwikkelaars queries verkennen en testen, wat productiviteit en foutoplossing verbetert.

GraphQL is populair geworden vanwege zijn flexibiliteit en de mogelijkheid om dataverzoeken te stroomlijnen, waardoor het een ideale keuze is voor applicaties met complexe databehoeften.

## GraphQL api oproepen in Laravel vanuit de backend met PHP.
Om een ​​Laravel-project te maken dat communiceert met de GraphQL API met behulp van JavaScript in de frontend, moeten we volgende zaken doen:

1. Laravel project aanmaken
2. Gebruik JavaScript om de Flask API aan te roepen
3. Creëer de nodige Laravel controllers
4. Configureer routes

### Laravel project aanmaken
```bash
composer create-project laravel/laravel consumeApi
# change database type to 'mysql' in .env
cd /consumeApi
php artisan migrate
# start onze website, host 0.0.0.0 is nodig om correct met docker te werken
php artisan serve --host 0.0.0.0
```

### 6: Demo 5
We een endpoint voorzien in de `routes/web.php` en we gaan de [`PHP GraphQL Client`](https://github.com/softonic/graphql-client) module gebruiken om de GraphQL queries uit te voeren. (`composer require softonic/graphql-client`):

<details open>
    <summary><i><b>Klik hier om de code te zien/verbergen voor `routes/web.php`</b></i></summary>
    <p>


```php
<?php

use Illuminate\Support\Facades\Route;
use Illuminate\Http\Request;
use Softonic\GraphQL\ClientBuilder;

Route::get('/', function () {
    return view('welcome');
});

Route::get('/graphQl_1', function () {
    # Create the client with the correct URL for the graphQl api
    $client = ClientBuilder::build('https://spacex-production.up.railway.app/');
    # Define the correct query
    $query = 'query ExampleQuery {
        company {
          ceo
        }
    }';
    # Define the variables, if none needed make this an empty array
    $variables = [];
    # Execute the request
    $response = $client->query($query,$variables);
    # Log the response
    dd($response);
});

Route::get('/graphQl_2', function () {
    $client = ClientBuilder::build('https://spacex-production.up.railway.app/');
    # The beauty of QraphQL is that you can query just the data you need in the client, so no under- or overfetching
    $query = 'query ExampleQuery {
            company {
                ceo
            }
            roadster {
                mars_distance_km
            }   
        }';

    $variables = [];

    $response = $client->query($query,$variables);
    dd($response);
});

Route::get('/graphQl_3', function () {
    $client = ClientBuilder::build('https://spacex-production.up.railway.app/');

    $query = 'query Query($dragonId: ID!) {
                dragon(id: $dragonId) {
                    active
                    description
                    first_flight
                }
            }';
    # Define the variables in JSON format
    $variables = ["dragonId"=> "5e9d058759b1ff74a7ad5f8f"];

    $response = $client->query($query,$variables);
    # Unpack the response inside of PHP
    dd($response->getData()["dragon"]);
});
```
</p>
</details>

