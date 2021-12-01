
// d3.json(piechartDataUrl).then(function createPlotly(data) {
//     console.log(data);

//     // Create a bar graph using index
//     var DataSPA = data[0]['Total']
//     var DataSwim = data[1]['Total']
//     var DataMassage = data[2]['Total']
//     var DataSauna = data[3]['Total']
//     var DataGym = data[4]['Total']
//     var DataMC = data[5]['Total']
//     var defaultData = [DataSPA,DataSwim,DataMassage,DataSauna,DataGym,DataMC ]
//     console.log(defaultData)
//     var label=['SPA','Swim','Massage','Sauna','Gym', 'Movie center']


//     var piedata = [
//         // {
//         //   x: defaultData,
//         //   y: label,
//         //   type: "bar",
//         //   orientation: "h",
//         // }
  
//         {
//           values: defaultData,
//           labels: label,
//           type: "pie",
  
//         }
//       ];
    
//       var pieLayout = {
//         title: `service profit ${dropdownValue}`,
//         xaxis: { title: "Month" },
//         height: 400,
//         width: 500
//       };
    
//       Plotly.newPlot("pie", piedata, pieLayout);






// })