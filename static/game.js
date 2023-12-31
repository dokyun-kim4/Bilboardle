let guesses = 0;
document.getElementById("guess-form").addEventListener("submit", function (event) {
    event.preventDefault();
    submitGuess();
});



function submitGuess() {
    const guessInput = document.getElementById("guess-input");
    const guess = guessInput.value;
    guesses++;
    console.log(guesses)


    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/check_guess", true);
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                const response = JSON.parse(xhr.responseText);
                updatePage(response.result);
            } else {
                console.error("Error:", xhr.status);
            }
        }
    };

    const data = JSON.stringify({ guess: guess });
    xhr.send(data);
}

function updatePage(result) {
    const resultDiv = document.getElementById("result");
    const options = { year: 'numeric', month: 'numeric', day: 'numeric' };
    // resultDiv.textContent = ""; // Clear previous result

    const dictionary = result;
    const rowDiv = document.createElement("div");
    rowDiv.classList.add("row")

    for (const key in dictionary) {
        const valueDiv = document.createElement("div");
        valueDiv.classList.add("square");

        if (dictionary[key][1] == true) {
            valueDiv.style.backgroundColor = "#4D8B31";
            valueDiv.textContent = dictionary[key][0];
        }
        else if (dictionary[key][1] == false) {
            valueDiv.style.backgroundColor = "#d64045";
            valueDiv.textContent = dictionary[key][0];
        }
        else if (dictionary[key][1] == "up") {
            valueDiv.style.backgroundColor = "#ED9B40";
            valueDiv.textContent = dictionary[key][0] + " ⬆";
        }
        else {
            valueDiv.style.backgroundColor = "#ED9B40";
            valueDiv.textContent = dictionary[key][0] + " ⬇";
        }

        rowDiv.appendChild(valueDiv);
        rowDiv.appendChild(document.createTextNode(" "));
    }

    resultDiv.appendChild(rowDiv);


    if (guesses == 6) {
        openModal();
    }

}

function openModal() {
    const modal = document.getElementById('myModal');
    modal.style.display = 'block';
}

function closeModal() {
    const modal = document.getElementById('myModal');
    modal.style.display = 'none';
}