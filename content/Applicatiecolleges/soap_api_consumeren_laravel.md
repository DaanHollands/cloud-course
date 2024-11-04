---
title: "SOAP api consumeren in laravel"
weight: 8
author: Arne Duyver
draft: false
---

## SOAP API (Simple Object Access Protocol)
- **Protocol:** SOAP is een strikt protocol gebaseerd op XML, dat een specificatie biedt voor berichtenuitwisseling.
- **Taalonafhankelijk:** Kan gebruikt worden met elke programmeertaal die XML kan verwerken.
- **Transport:** SOAP gebruikt voornamelijk **HTTP**, maar kan ook andere protocollen gebruiken zoals **SMTP**.
- **Berichtenformaat:** SOAP-berichten zijn volledig XML-gebaseerd en hebben een vast formaat.
- **Veiligheid:** SOAP ondersteunt uitgebreide beveiligingsprotocollen zoals **WS-Security** voor betere beveiliging, en heeft ingebouwde ondersteuning voor **ACID-transacties**.
- **Stateful:** SOAP kan stateful operaties ondersteunen, wat betekent dat de server informatie over een sessie kan onthouden tussen verzoeken.

### REST API (Representational State Transfer)
- **Architectuurstijl:** REST is een flexibele architectuurstijl die een reeks aanbevelingen biedt voor het ontwerpen van API's, zonder een strikt protocol.
- **Taalonafhankelijk:** Net als SOAP kan REST in elke programmeertaal worden gebruikt, zolang het HTTP ondersteunt.
- **Transport:** REST gebruikt **HTTP** als transportlaag en gebruikt vaak standaard HTTP-methoden zoals **GET**, **POST**, **PUT**, **DELETE**.
- **Berichtenformaat:** REST is flexibeler in termen van het berichtenformaat, en ondersteunt **JSON**, **XML**, **HTML**, of zelfs platte tekst.
- **Veiligheid:** REST vertrouwt op de veiligheidsmechanismen van het HTTP-protocol, zoals **SSL/TLS**.
- **Stateless:** REST API's zijn **stateless**, wat betekent dat elke verzoek onafhankelijk is en de server geen informatie onthoudt over eerdere verzoeken.

### Belangrijkste Verschillen
| Kenmerk              | SOAP                      | REST                    |
|----------------------|---------------------------|-------------------------|
| **Protocol/Architectuur** | Strict protocol (XML-based) | Flexibele architectuur  |
| **Berichtenformaat**  | Alleen XML                | JSON, XML, HTML, etc.   |
| **Transportprotocol** | HTTP, SMTP, andere        | HTTP                    |
| **Beveiliging**       | WS-Security, ACID         | SSL/TLS                 |
| **Stateful/Stateless**| Stateful                  | Stateless               |

### Wanneer SOAP kiezen?
- Bij **complexe transactieprocessen** (bijv. bankieren) die sterk beveiligd en stateful moeten zijn.
  
### Wanneer REST kiezen?
- Voor **webservices** waar snelheid, eenvoud en flexibiliteit belangrijk zijn, zoals in **mobiele applicaties**.

## SOAP api oproepen in Laravel vanuit de frontend met Javascript
Om een ​​Laravel-project te maken dat communiceert met de SOAP API met behulp van JavaScript in de frontend, moeten we volgende zaken doen:

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

### Laravel views en Javascript calls
We gebruiken JavaScript (met fetch) om de Flask REST API op te roepen.
Maak een nieuwe lay-out als deze niet bestaat en voeg vervolgens de benodigde HTML-structuur en een tijdelijke aanduiding voor de inhoud toe: `views/soap.blade.php`.

Je kan de [Wizdler extentie](https://chromewebstore.google.com/detail/wizdler/oebpmncolmhiapingjaagmapififiakb) gebruiken om na te gaan hoe de body er juist moet uitzien.
<details open>
    <summary><i><b>Klik hier om de code te zien/verbergen voor `views/soap.blade.php`</b></i></summary>
    <p>

```php
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SOAP Request Example</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      margin: 20px;
    }

    input {
      margin: 5px;
    }

    #result {
      margin-top: 20px;
      font-weight: bold;
    }
  </style>
</head>

<body>
  <h1>Add Two Numbers Using SOAP</h1>
  <label for="num1">Number 1:</label>
  <input type="number" id="num1" value="1"><br>

  <label for="num2">Number 2:</label>
  <input type="number" id="num2" value="2"><br>

  <button id="addButton">Add</button>

  <div id="result"></div>

  <script>

    async function makeSoapRequest(intA, intB) {
      const proxyUrl = '' //+ 'https://crossorigin.me/';
      const url = proxyUrl + 'http://www.dneonline.com/calculator.asmx';
      const soapRequest = `
        <?xml version="1.0" encoding="utf-8"?>
        <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                       xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                       xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
            <soap:Body>
                <Add xmlns="http://www.dneonline.com/calculator/">
                    <intA>${intA}</intA>
                    <intB>${intB}</intB>
                </Add>
            </soap:Body>
        </soap:Envelope>`;

      try {
        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'text/xml; charset=utf-8',
            'SOAPAction': 'http://www.dneonline.com/calculator/Add'
          },
          body: soapRequest
        });

        const text = await response.text();
        const parser = new DOMParser();
        const xmlDoc = parser.parseFromString(text, 'text/xml');
        const result = xmlDoc.getElementsByTagName('AddResult')[0].textContent;

        // Display the result in the div
        document.getElementById('result').textContent = `The result of adding ${intA} and ${intB} is: ${result}`;
      } catch (error) {
        console.error('Error making SOAP request:', error);
        document.getElementById('result').textContent = 'Error making SOAP request';
      }
    }

    document.getElementById('addButton').addEventListener('click', () => {
      const num1 = document.getElementById('num1').value;
      const num2 = document.getElementById('num2').value;
      makeSoapRequest(num1, num2);
    });
  </script>
</body>

</html>
```

</p>
</details>


### Routes definiëren

Definieer in `routes/web.php` een route om de users view te laden.

```php
use Illuminate\Support\Facades\Route;

Route::get('/soapTest', function () {
    return view('soap');
});
```


## Call maken vanuit de backend anders CORS problemen
### 6: Demo 4
Dan moeten we een extra endpoint voorzien in de `routes/web.php` en we gaan weer de Guzzle module gebruiken om de call te doen naar de SOAP service (`composer require guzzlehttp/guzzle`):

<details open>
    <summary><i><b>Klik hier om de code te zien/verbergen voor `routes/web.php`</b></i></summary>
    <p>


```php
<?php

use Illuminate\Support\Facades\Route;
use Illuminate\Http\Request;
use GuzzleHttp\Client;

Route::get('/', function () {
    return view('welcome');
});

Route::get('/soap', function () {
    return view('soap');
});

Route::get('/soapAdd', function () {
    $num1 = request('num1');
    $num2 = request('num2');
    try {
        // URL of the SOAP service
        $wsdl = "http://www.dneonline.com/calculator.asmx?wsdl";
        
        // Create a new SoapClient instance
        $client = new SoapClient($wsdl);
    
        // Call the 'Add' method with parameters
        $params = [
            'intA' => 1,
            'intB' => 2,
        ];
        
        // Perform the SOAP request
        $response = $client->__soapCall('Add', [$params]);
        
        // Display the response
        $result = $response->AddResult;
         return response()->json(['result' => $result]);
    } catch (SoapFault $e) {
        return response()->json(['SOAP Error:' => $e->getMessage()]);
    }  
});
```
</p>
</details>

Nu updaten we de view om genbruik te maken van dit nieuwe endpoint:
<details open>
    <summary><i><b>Klik hier om de code te zien/verbergen voor `views/soap.blade.php`</b></i></summary>
    <p>

```php
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SOAP Request Example</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      margin: 20px;
    }

    input {
      margin: 5px;
    }

    #result {
      margin-top: 20px;
      font-weight: bold;
    }
  </style>
</head>

<body>
  <h1>Add Two Numbers Using SOAP</h1>
  <label for="num1">Number 1:</label>
  <input type="number" id="num1" value="1"><br>

  <label for="num2">Number 2:</label>
  <input type="number" id="num2" value="2"><br>

  <button id="addButton">Add</button>

  <div id="result"></div>

  <script>
    // Function to fetch users and populate the table
    function test(num1,num2) {
      var formData = {
        num1: 1,
        num2: 2,
      };
      // Hier doen we dus een oproep naar het lokale endpoint
      fetch(`/soapAdd?num1=${num1}&num2=${num2}`)
      .then(response => response.json())
      .then(data => {
        console.log(data.result)
        document.getElementById('result').innerHTML = data.result
      })
      .catch(error => {
        console.error('Error fetching users:', error)
        document.getElementById('result').innerHTML = error
      });
    }


    document.getElementById('addButton').addEventListener('click', () => {
      const num1 = parseInt(document.getElementById('num1').value, 10);
      const num2 = parseInt(document.getElementById('num2').value, 10);
      test(num1, num2);
    });
  </script>
</body>
</html>

```

</p>
</details>

