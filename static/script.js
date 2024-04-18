// Add event listener for searchButton on click
const btn = document.querySelector('.search-button')
const spinner = document.querySelector('.spinner')
const stat = document.querySelector('.status')

const mic = document.querySelector('.mic')
// Add event listener for form submission
document.querySelector('form').addEventListener('submit', function(e) {
    e.preventDefault(); // Prevent the default form submission behavior


    spinner.classList.remove('visually-hidden')
    btn.classList.remove('btn-outline-danger')
    btn.classList.add('btn-danger')
    btn.classList.add('disabled')
    stat.innerHTML = 'Loading...'

    // Prepare FormData with inputs for file and text
    var formData = new FormData(this);

    // Make an AJAX request to the server
    fetch('/', { // Make sure this URL matches your Flask route
        method: 'POST',
        body: formData, // Send the form data
    })
    .then(response => response.json()) // Parse JSON response
    .then(data => {
        // Here, 'data' is the JSON object returned from the server
        // Construct the HTML for results
        let resultHtml = '';
        let ingredientsHtml = `<div class='card border-success mb-3' style='max-width: 18rem;'>
            <div class='card-header'>Ingredients found:</div>
            <ul class='list-group list-group-flush'>`;
        let recipesHtml = "<div class='row row-cols-1 row-cols-sm-2 row-cols-md-3 g-3'>";
        if (data.ingredients_found) {
            data.ingredients_found.forEach(ingredient => {
                ingredientsHtml += `<li class="list-group-item">${ingredient}</li>`;
            });
        } else {
            ingredientsHtml += "<li class='list-group-item'>No ingredients found.</li>";
        }
        ingredientsHtml += "</ul></div>";

        if (data.recipes) {
            data.recipes.forEach(recipe => {
                recipesHtml += `<div class="col">
                    <div class="card shadow-sm">
                    <img src="${recipe.image}" class="card-img-top" alt="Image of ${recipe.title}" width="100%" height="225" role="img" aria-label="Placeholder: ${recipe.title}" preserveAspectRatio="xMidYMid slice" focusable="false">
                    <div class="card-header">
                        <div class="d-flex justify-content-between align-items-center">
                            <div class="btn-group">
                                <button type="button" class="btn btn-sm btn-outline-secondary" data-bs-toggle="button" >Bookmark</button>
                            </div>
                            <small class="text-body-secondary" id="time">${recipe.servings} servings</small>
                            <small class="text-body-secondary" id="time">${recipe.time} minutes</small>
                        </div>
                    </div>
                    <div class="card-body">
                        <h5 class="card-title" id="title">${recipe.title}</h5>
                        <p class="card-text" id="description">${recipe.description}</p>
                    </div>
                    <ul class="list-group list-group-flush">
                        <li class="list-group-item">Ingredients:</li>
                        <li class="list-group-item card-body">
                    <ul>`;
                recipe.ingredients.forEach(ingredient => {
                    recipesHtml += `<li>${ingredient}</li>`;
                });
                recipesHtml += `</ul>
                    </li>
                    <li class="list-group-item">Steps:</li>
                    <li class="list-group-item card-body">
                    <ul>`;
                recipe.steps.forEach(step => {
                    recipesHtml += `<li>${step}</li>`;
                });
                recipesHtml += `</ul>
                            </li>
                        </ul>
                        <div class="card-footer">
                            <small class="text-muted">Written by ${recipe.author}</small>
                        </div>
                        </div>
                        </div>`;
            });
            recipesHtml += `</div></div>`;
        }
        // Append results to a container in your HTML
        resultHtml += ingredientsHtml + recipesHtml;
        document.getElementById('results').innerHTML = resultHtml;

        spinner.classList.add('visually-hidden')
        btn.classList.remove('btn-danger')
        btn.classList.add('btn-outline-danger')
        btn.classList.remove('disabled')
        stat.innerHTML = 'Search'
    })
    .catch(error => console.error('Error:', error)); // Handle errors
    
});


const recordBtn = document.getElementById('mic');
let mediaRecorder;
let recording = false;
let audioChunks = [];

recordBtn.addEventListener('click', () => {
    
    if (!recording) {
        mic.classList.remove('btn-outline-success');
        mic.classList.add('btn-success');
        // Start recording
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(stream => {
                mediaRecorder = new MediaRecorder(stream);
                mediaRecorder.start();
                recordBtn.textContent = 'Stop Recording';

                mediaRecorder.addEventListener("dataavailable", event => {
                    audioChunks.push(event.data);
                });

                mediaRecorder.addEventListener("stop", () => {
                    const audioBlob = new Blob(audioChunks, { 'type' : 'audio/wav' });
                    sendAudioToServer(audioBlob);
                    audioChunks = [];
                    recordBtn.textContent = 'Start Recording';
                });

                recording = true;
            })
            .catch(error => console.error('Error accessing media devices.', error));
    } else {
        mic.classList.remove('btn-success');
        mic.classList.add('btn-outline-success');
        // Stop recording
        mediaRecorder.stop();
        recording = false;
    }
});

function sendAudioToServer(audioBlob) {
    const formData = new FormData();
    formData.append("audio", audioBlob);
    fetch('/audio', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        let resultHtml = '';
        let ingredientsHtml = `<div class='card border-success mb-3' style='max-width: 18rem;'>
            <div class='card-header'>Ingredients found:</div>
            <ul class='list-group list-group-flush'>`;
        let recipesHtml = "<div class='row row-cols-1 row-cols-sm-2 row-cols-md-3 g-3'>";
        if (data.ingredients_found) {
            data.ingredients_found.forEach(ingredient => {
                ingredientsHtml += `<li class="list-group-item">${ingredient}</li>`;
            });
        } else {
            ingredientsHtml += "<li class='list-group-item'>No ingredients found.</li>";
        }
        ingredientsHtml += "</ul></div>";

        if (data.recipes) {
            // recipesHtml += "<div class='row row-cols-1 row-cols-sm-2 row-cols-md-3 g-3'>";
            data.recipes.forEach(recipe => {
                recipesHtml += `<div class="col">
                    <div class="card shadow-sm">
                    <img src="${recipe.image}" class="card-img-top" alt="Image of ${recipe.title}" width="100%" height="225" role="img" aria-label="Placeholder: ${recipe.title}" preserveAspectRatio="xMidYMid slice" focusable="false">
                    <div class="card-header">
                        <div class="d-flex justify-content-between align-items-center">
                            <div class="btn-group">
                                <button type="button" class="btn btn-sm btn-outline-secondary" data-bs-toggle="button" >Bookmark</button>
                            </div>
                            <small class="text-body-secondary" id="time">${recipe.servings} servings</small>
                            <small class="text-body-secondary" id="time">${recipe.time} minutes</small>
                        </div>
                    </div>
                    <div class="card-body">
                        <h5 class="card-title" id="title">${recipe.title}</h5>
                        <p class="card-text" id="description">${recipe.description}</p>
                    </div>
                    <ul class="list-group list-group-flush">
                        <li class="list-group-item">Ingredients:</li>
                        <li class="list-group-item card-body">
                    <ul>`;
                recipe.ingredients.forEach(ingredient => {
                    recipesHtml += `<li>${ingredient}</li>`;
                });
                recipesHtml += `</ul>
                    </li>
                    <li class="list-group-item">Steps:</li>
                    <li class="list-group-item card-body">
                    <ul>`;
                recipe.steps.forEach(step => {
                    recipesHtml += `<li>${step}</li>`;
                });
                recipesHtml += `</ul>
                            </li>
                        </ul>
                        <div class="card-footer">
                            <small class="text-muted">Written by ${recipe.author}</small>
                        </div>
                        </div>
                        </div>`;
            });
            recipesHtml += `</div></div>`;
        }
        // Append results to a container in your HTML
        resultHtml += ingredientsHtml + recipesHtml;
        document.getElementById('results').innerHTML = resultHtml;
    })
    .catch(error => console.error('Error:', error));
}