/* This script is meant to modify the colored bar, text and vertical bar into the air quality widget. 
It takes the value from the html element and set to them the corresponding class to style them.  */
document.addEventListener('DOMContentLoaded', () => {
    let bar = document.querySelector('.bar');
    let sections = bar.querySelectorAll('.section');
    let aqi_details_sections = document.querySelectorAll('.aqi-details-sections')

    let c = {
        'class': null,
        'text': null
    };

    // Breakpoints in ug/m3
    let breakpoints = {
        'o3': [108, 140, 170, 210, 400],
        'pm2_5': [12, 35.4, 55.4, 150.4, 250.4],
        'pm10': [54, 154, 254, 354, 424],
        'co': [503.8, 1074.3, 1419.8, 1763.3, 3480.8, 5770.8],
        'so2': [91.7, 196.5, 484.7, 796.48, 1582.48, 2630.48],
        'no2': [66.25, 128, 450, 811.25, 1561.25, 2561.25]
    }

    // Getting the right case for setting the bar color
    switch (bar.dataset.active) {
        case "1":
            c['class'] = "active-good";
            c['text'] = 'good'
            break;
        case "2":
            c['class'] = "active-moderate";
            c['text'] = 'moderate'
            break;
        case "3":
            c['class'] = "active-poor";
            c['text'] = 'poor'
            break;
        case "4":
            c['class'] = "active-unhealty";
            c['text'] = 'unhealty'
            break;
        case "5":
            c['class'] = "active-very-unhealty";
            c['text'] = 'very unhealty'
            break;
        case "6":
            c['class'] = "active-hazardous";
            c['text'] = 'hazardous'
            break;

    }

    // Adding the right class on switch result
    for (let i = 0; i < bar.dataset.active; i++) {
        sections[i].classList.add(c['class']);
    }

    // Adding the right text description on switch result
    document.querySelector('#aqi-text').innerHTML = c['text']

    // Loop for vertical colored bar
    aqi_details_sections.forEach(section => {
        let i = null
        // Comparing the data value with the corresponding breakpoints and break when the value is less than the breakpoint
        breakpoints[section.dataset.aqiType].every((e, index) => {
            if (section.dataset.value <= e) {
                i = index + 1;
                return false;
            }
            return true;
        })

        // Selecting the right case with the index from the breakpoint check
        switch (i) {
            case 1:
                c['class'] = "active-good";
                break;
            case 2:
                c['class'] = "active-moderate";
                break;
            case 3:
                c['class'] = "active-poor";
                break;
            case 4:
                c['class'] = "active-unhealty";
                break;
            case 5:
                c['class'] = "active-very-unhealty";
                break;
            case 6:
                c['class'] = "active-hazardous";
                break;
        }

        // Adding the right class on the switch result
        section.classList.add(c['class'])
    })

})