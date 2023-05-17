const yearSelect = document.getElementById('year');
const filterForm = document.getElementById('filterForm');

let myChart = document.getElementById('myChart');
console.log(myChart);

window.addEventListener('load', async () => {
	const response = await fetch('chart/filter-options');
	const jsonData = await response.json();
	jsonData.options.forEach(option => {
		opt = document.createElement('option');
		opt.value = option;
		opt.text = option;
		yearSelect.add(opt);
	});

	loadAllCharts(yearSelect.firstChild.value);
});

filterForm.addEventListener('submit', e => {
	e.preventDefault();

	const year = yearSelect.value;
	loadAllCharts(year);
});

const loadChart = async (chart, endpoint) => {
	const response = await fetch(`chart/${endpoint}`);
	const jsonData = await response.json();
	console.log(jsonData);

	const title = jsonData.title;
	const scaleX = jsonData.scaleX;
	const scaleY = jsonData.scaleY;
	const series = jsonData.series;

	let chartConfig = {
		type: 'bar',
		title,
		scaleX,
		scaleY,
		plot: {
			animation: {
				effect: '11',
				method: '3',
				sequence: '2',
				speed: 10,
			},
		},
		series,
		noData: {
			text: 'Fetching remote data...',
			backgroundColor: '#eeeeee',
			fontSize: 18,
		},
	};

	zingchart.render({
		id: chart.id,
		data: chartConfig,
	});

	// console.log(myConfig);
};

const loadAllCharts = year => {
	loadChart(myChart, `projects/${year}`);
};
