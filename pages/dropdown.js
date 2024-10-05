async function loadCSV() {
    const response = await fetch('data-jBXGd.csv');
    const data = await response.text();
    return data;
}


function parseCSV(data) {
    const lines = data.split('\n').map(line => line.split(','));
    const headers = lines[0]; // 
    const statesInfo = {};

    for (let i = 1; i < lines.length; i++) {
        const state = lines[i][0].trim();
        if (state) {
            statesInfo[state] = headers.slice(1).map((header, index) => `${header}: ${lines[i][index + 1].trim()}`).join('<br>');
        }
    }
    return statesInfo;
}

async function initialize() {
    const csvData = await loadCSV();
    const statesInfo = parseCSV(csvData);

    const statesDropdown = document.getElementById('states');

    Object.keys(statesInfo).forEach(state => {
        const option = document.createElement('option');
        option.value = state;
        option.textContent = state;
        statesDropdown.appendChild(option);
    });

    statesDropdown.addEventListener('change', function() {
        const selectedState = this.value;
        const infoContainer = document.getElementById('info');

        if (selectedState) {
            infoContainer.innerHTML = statesInfo[selectedState]; 
        } else {
            infoContainer.innerHTML = ''; 
        }
    });
}

initialize();
