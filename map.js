import {Map as LeafletMap, TileLayer, GeoJSON } from 'leaflet';

const map = new LeafletMap('map').setView([41.88, -87.62], 13);

const tiles = new TileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
	maxZoom: 19,
	attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

let geojson;

function getColor(d) {
	return d > 9000 ? '#800026' :
	       d > 7000  ? '#BD0026' :
	       d > 6000  ? '#E31A1C' :
	       d > 5000  ? '#FC4E2A' :
	       d > 4000   ? '#FD8D3C' :
	       d > 3000   ? '#FEB24C' :
	       d > 2000   ? '#FED976' :
	                  '#FFEDA0';
}

function style(feature) {
	return {
		fillColor: getColor(feature.properties.density),
		weight: 2,
		opacity: 1,
		color: 'white',
		dashArray: '3',
		fillOpacity: 0.7
	};
}

function highlightFeature(e) {
	const layer = e.target;

	layer.setStyle({
		weight: 5,
		color: '#666',
		dashArray: '',
		fillOpacity: 0.7
	});

	layer.bringToFront();
}

function resetHighlight(e) {
	geojson.resetStyle(e.target);
}

function connectMapAndZoom(e) {
	const layer = e.target;
	const geoid = String(layer.feature.properties.geoid10);
	document.getElementById("geoid").textContent = "Census Tract: " + geoid;
	loadTractData(geoid);
	map.fitBounds(e.target.getBounds());
}

function onEachFeature(feature, layer) {
	layer.on({
		pointerover: highlightFeature,
		pointerout: resetHighlight,
		click: connectMapAndZoom
	});
}
//loading tract data
function loadTractData(geoid) {
    console.log("Selected GEOID:", geoid);

    fetch(`http://127.0.0.1:5000/api/tract/${geoid}`)
    .then(response => {
        console.log("Response:", response.status);

        if (!response.ok) {
            throw new Error("Couldn't get the data");
        }

        return response.json();
    })
    .then(data => {
        console.log("Received data:", data);

        updateCharts(data);
    })
    .catch(error => {
        console.error("Error:", error);
    });
}

function getIncomeTotal(row, columns) {
    return columns.reduce((total, column) => {
        return total + (Number(row[column]) || 0);
    }, 0);
}

function updateCharts(data) {
	// sorts the data by year from oldest to newest
	data.permits.sort((a,b) =>a.Year - b.Year);
	data.income.sort((a,b) =>a.Year - b.Year);
	data.race.sort((a,b) =>a.Year - b.Year);

	//create an array of all years in permit dataset
	const permitYears = data.permits.map(row => row.Year);

	//create array of the number of permits issued
	const permitCounts = data.permits.map(row => row.permit_count);

	// array of total reported construction cost
	const constructionCost = data.permits.map(row => row.total_cost);

	// residental units added or removed
	const residentUnits = data.permits.map(row => row.resident);

	//get years from income chart
	const incomeYears = data.income.map(row => row.Year);

	//putting income ranges into lists
	//below 25k
	const lowerIncome = [
		"Under10kEst",
		"10k-14kEst",
		"15k-19kEst",
		"20k-24kEst"
	];

	//25k-99k
	const middleIncome = [
		"25k-29kEst",
		"30k-34kEst",
		"35k-39kEst",
		"40k-44kEst",
		"45k-49kEst",
		"50k-59kEst",
		"60k-74kEst",
		"75k-99kEst"
	];

	const higherIncome = [
    "100k-124kEst",
    "125k-149kEst",
    "150k-199kEst",
    "Above200kEst"
	];

	//calculates each income group
	const lowerIncomeTot = data.income.map(row => getIncomeTotal(row, lowerIncome));	

	const middleIncomeTot = data.income.map(row => getIncomeTotal(row, middleIncome));

	const higherIncomeTot = data.income.map(row => getIncomeTotal(row, higherIncome));

	//get years from race chart
	const raceYears = data.race.map(row => row.Year);

	const populationTotals = data.race.map(row => row.TotalEst);

	// array of objects defining racial groups
	const raceGroups = [
		{ name: "Hispanic", column: "HispTotalEst" },
		{ name: "Non-Hispanic White", column: "NotHispWhiteEst" },
		{ name: "Non-Hispanic Black", column: "NotHispBlackEst" },
		{ name: "Non-Hispanic Asian", column: "NotHispAsianEst" },
		{ name: "Non-Hispanic Native American", column: "NotHispNativeORalaskanEst" },
		{ name: "Non-Hispanic Pacific Islander", column: "NotHispNativeHaWaiiORPacificEst" },
		{ name: "Non-Hispanic Other Race", column: "NotHispOtherRaceEst" },
		{ name: "Non-Hispanic Two or More Races", column: "NotHispTwoPlusEst" }
	];


	const raceLines = raceGroups.map( group => {
		//population estimate for that racial group for every year
		const counts = data.race.map(row => Number(row[group.column]) || 0);

		//gets percentages of the total population represented by current racial group
		const percentages = data.race.map((row,index) => {
			const totalPop = Number(row.TotalEst) || 0;
			if (totalPop == 0) return 0;
			return (counts[index] / totalPop) * 100

		});

		//creates a line for each racial group
		return {
			x: raceYears,
			y: percentages,
			customdata: counts,
			type: "scatter",
			mode: "lines+markers",
			name: group.name,
			hovertemplate:
				"%{fullData.name}<br>" +
				"Year: %{x}<br>" +
				"Population: %{customdata:,.0f}<br>" +
				"Percentage: %{y:.1f}%<extra></extra>"
		};
	});

	//creating the permits chart with plotly
	Plotly.react("permits-chart", [
		{
			x: permitYears,
			y: permitCounts,
			type: "scatter",
			mode: "lines+markers",
			name: "Permits Issued"
		},
		{
			x: permitYears,
			y: constructionCost,
			type: "scatter",
			mode: "lines+markers",
			name: "Construction cost",
			yaxis: "y2"
		},
		{
			x: permitYears,
			y: residentUnits,
			type: "scatter",
			mode: "lines+markers",
			name: "Residential units added/removed"
		}
	], 
		{
			title: "Building Permits Over Time",
			xaxis: {title: "Year"},
			yaxis: {title: "Permits / Residential Units"},
			yaxis2: {
				title: "Reported Construction Cost ($)",
				overlaying: "y",
				side: "right"
			},
			autosize: true,
			legend: {
				orientation: "h",
				y: -0.25,
				x: 0.5,
				xanchor: "center",
				font: {
					size: 11
				}
			}
		}, {
    responsive: true
}
	);

	//create the income chart
	Plotly.react("income-chart", [
		{
			x: incomeYears,
			y: lowerIncomeTot,
			type: "scatter",
			mode: "lines+markers",
			name: "Under $25,000"
		},
		{
			x: incomeYears,
			y: middleIncomeTot,
			type: "scatter",
			mode: "lines+markers",
			name: "$25,000 - $99,000"
		},
		{
			x: incomeYears,
			y: higherIncomeTot,
			type: "scatter",
			mode: "lines+markers",
			name: "above $99,000"
		}
	],
		{
			title: "Household Income Over Time",
			xaxis: {title: "Year"},
			yaxis: {title: "Estimated Numberr of Households"},
			autosize: true, 
			legend: {
				orientation: "h",
				y: -0.25,
				x: 0.5,
				xanchor: "center",
				font: {
					size: 11
				}
			}
		}, {
    responsive: true
}
	
	);

	Plotly.react("race-chart", raceLines, {
		title: "Racial Demographics Over Time",
		xaxis: {title: "Year"},
		yaxis: {
			title: "Percentage of Population",
			ticksuffix: "%"
		},
		autosize: true,
	});

	//population chart
	Plotly.react("population-chart", [{
		x:raceYears,
		y:populationTotals,
		type: "scatter",
		mode: "lines+markers",
		name: "Total Population"
	}], {
		title: "Population Changes Over Time",
		xaxis: { title: "Year" },
		yaxis: { title: "Total Population" },
		autosize: true,
		legend: {
				orientation: "h",
				y: -0.25,
				x: 0.5,
				xanchor: "center",
				font: {
					size: 11
				}
			}
	}, {
    responsive: true
});
}


fetch('Data/census_tracts_density.geojson')
.then(response => response.json())
.then(data => {
    geojson = new GeoJSON(data, {style: style, onEachFeature: onEachFeature}).addTo(map);
});
