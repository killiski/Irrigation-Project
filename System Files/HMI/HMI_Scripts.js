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












// --------------------------------------------------------- 
// --------------------------------------------------------- 
// --------------------------------------------------------- 
// --------------------------------------------------------- 
// --------------------------------------------------------- 

    function toggleWifiInput() { // show wifi pop up => i want it to display over the page not inline
        const wifiInputDiv = document.getElementById("wifiInput");
        wifiInputDiv.style.display = wifiInputDiv.style.display === "none" ? "block" : "none";
    }

    function updateWifiValues() { // input wifi values => I want to clear input boxes after to show feedback and disable submit until response
        const ssid = document.getElementById("ssid").value;
        const password = document.getElementById("password").value;
        const xhr = new XMLHttpRequest();
        xhr.open("POST", "/updateWifi", true);
        xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4 && xhr.status === 200) {
                const response = JSON.parse(xhr.responseText);
                alert("Connected to " + response.ssid);
                fetchValues(); // Fetch updated values
            }
        };
        xhr.send(`ssid=${ssid}&password=${password}`);
    }

    function fetchValues() {
        const xhr = new XMLHttpRequest();
        xhr.open("GET", "/values", true);
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4 && xhr.status === 200) {
                const response = JSON.parse(xhr.responseText);
                // Display fetched values
                document.getElementById("displayValue1").innerText = response.value1;
                document.getElementById("displayValue2").innerText = response.value2;

                // Set slider values based on fetched values
                // document.getElementById("sliderValue1").value = response.value1;
                // document.getElementById("sliderValue2").value = response.value2;
            }
        };
        xhr.send();
    }

    function scanNetworks() {
        const xhr = new XMLHttpRequest();
        xhr.open("GET", "/scan", true);
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4 && xhr.status === 200) {
                const response = JSON.parse(xhr.responseText);
                const ssidSelector = document.getElementById("ssid");
                ssidSelector.innerHTML = ''; // Clear previous SSIDs
                response.networks.forEach(function(network) {
                    const option = document.createElement('option');
                    option.value = network;
                    option.textContent = network;
                    ssidSelector.appendChild(option);
                });
            }
        };
        xhr.send();
    }

    function updateStoredValues() {
        const value1 = document.getElementById("sliderValue1").value;
        const value2 = document.getElementById("sliderValue2").value;
        const xhr = new XMLHttpRequest();
        xhr.open("POST", "/valuesUpdate", true);
        xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4 && xhr.status === 200) {
                fetchValues(); // Refresh displayed values after update
            }
        };
        xhr.send(`value1=${value1}&value2=${value2}`); // Send only slider values
    }

    setInterval(fetchValues, 5000);