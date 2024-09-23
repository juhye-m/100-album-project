console.log("let's get started!")

// margin object

// load data
initializePage();

function initializePage() {
    loadData().then(jsonData => {
        console.log(jsonData) // print to console to see if json data fetched properly
        displaySummaryInfo(jsonData);
        visualizeData(jsonData);  // If you plan to add visualizations
    }).catch(error => {
        console.error('Error loading data: ', error);
    });
}

// load data using d3.json and return a promise
function loadData() {
    return d3.json("../data/summary_analysis.json");
}


// display basic info
function displaySummaryInfo(jsonData) {
    // extract these fields from the json
    let avgDuration = jsonData.average_duration["0"]; // ["0"] because the value is wrapped in additional dict where the key is 0 (bc df conversion i think). perhaps more efficient to fix in the py later?
    let sumDuration = jsonData.sum_duration["0"];
    let avgTracks = jsonData.average_tracks["0"];
    let sumTracks = jsonData.sum_tracks["0"];

    // populate HTML
    document.getElementById("avg-duration").textContent = avgDuration;
    document.getElementById("sum-duration").textContent = sumDuration;
    document.getElementById("avg-tracks").textContent = avgTracks;
    document.getElementById("sum-tracks").textContent = sumTracks;

    console.log("hi new data")
}

// visualize
function visualizeData(jsonData) {
    // d3 visualization later
}

window.onload = function() {
    initializePage();  // execute after window is fully loaded
};

// create event handler

// bind event handler