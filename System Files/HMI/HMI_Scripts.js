let myChart; // Declare the chart variable to access it later

	
	
	function updateTime() {
		const now = new Date();
		const formattedTime = now.toISOString().slice(0, 19).replace('T', ' ');
		document.getElementById('time').textContent = formattedTime;
	}

	function togglePopup(event) {
		const popup = document.getElementById('wifi-popup');
		// Toggle popup visibility
		popup.style.display = popup.style.display === 'block' ? 'none' : 'block';
		// Prevent click event from closing the popup if clicking inside it
		event.stopPropagation();
	}

	function closePopup() {
		const popup = document.getElementById('wifi-popup');
		popup.style.display = 'none';
	}

	function submitInputs() {
		const inputs = document.querySelectorAll('.wifi-popup input');
		inputs.forEach(input => {
			console.log(input.value); // You can change this to whatever you want to do with the inputs
		});
		closePopup(); // Close the popup after submission
	}

	

	// Create the chart
	window.onload = () => {
		updateTime();
		setInterval(updateTime, 1000); // Update time every second
		
		const canvas = document.getElementById('myChart');
		

		const labels = Array.from({ length: 25 }, (_, hour) => new Date(2024, 0, 1, hour)); // Use Date objects directly
		const data = Array.from({ length: 25 }, () => 20 + Math.random() * 30); // Values between 20 and 30


		const ctx = canvas.getContext('2d');
		myChart = new Chart(ctx, {
			type: 'line',
			data: {
				labels: labels,
				datasets: [{
					label: 'Random Data',
					data: data,
					borderColor: 'rgba(75, 192, 192, 1)',
					borderWidth: 1,
					fill: false
				}]
			},
			options: {
				responsive: true,
				maintainAspectRatio: false, // Allow custom aspect ratio

				
				scales: {
					x: {
						type: 'time',
						time: {
							unit: 'hour',
							tooltipFormat: 'HH:mm',
							displayFormats: {
								hour: 'HH:mm' // Format for displaying hours
							},
						},
						title: {
							display: true,
							text: 'Time (24-hour format)',
							font: {
								size: 16 // Set title font size
							}
						},
						min: new Date(2024, 0, 1, 0),
						max: new Date(2024, 0, 1, 24),
					},
					y: {
						type: 'linear',
						beginAtZero: true,
						title: {
							display: true,
							text: 'Value (%)',
							font: {
								size: 20 // Set title font size
							}
						},
						ticks: {
							font: {
								size: 16 // Set y-axis tick font size
							},
							
						},
					},
				},
				plugins: {
					tooltip: {
						mode: 'index',
						intersect: false,
					},
					zoom: {
						limits: {
							x: { min: new Date(2024, 0, 1, 0), max: new Date(2024, 0, 1, 24), minRange: 3600000 }, // 1 hour in milliseconds
						},
						pan: {
							enabled: true,
							mode: 'x', // Enable panning only on the x-axis
							onPan({ chart, event }) {
								console.log("Panning:", event);
							}
						},
						zoom: {
							wheel: {
								enabled: true,
							},
							pinch: {
								enabled: true,
							},
							mode: 'x',
						}
					}
				}
			}
		});
	}