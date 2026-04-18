
export let DriverColoursGraph = {}
export function AssignDriverColours(DriversLen, Drivers){
  //Random colours function
  let array = []
  for (let i = 0; i < DriversLen; i++)
  {
    let num1 = Math.floor(Math.random() * (255 - 1 + 1)) + 1;
    let num2 = Math.floor(Math.random() * (255 - 1 + 1)) + 1;
    let num3 = Math.floor(Math.random() * (255 - 1 + 1)) + 1;
    

    num1 = num1.toString(16).padStart(2, '0')
    num2 = num2.toString(16).padStart(2, '0')
    num3 = num3.toString(16).padStart(2, '0')
    array[i] = "#" + num1 + num2 + num3
  }
  DriverColoursGraph = Object.values(DriverColoursGraph)
  for(let i = 0; i < DriversLen; i++)
  {
    Drivers[i].colour = array[i]
    DriverColoursGraph[Drivers[i].name] = array[i]
   
  }
  if (Drivers == undefined)
  {
    return null
  }
  return Drivers

}

export function SortDataForGraph(Data)
{
  let newRows = {}
  
  //we need to sort the data so its in individual rows for each date
  //Get all of the dates then just add all values that match that date
  Data.forEach(({timestamp}) => {
    if (!newRows[timestamp])
    {
      newRows[timestamp] = {timestamp}
     
    }
  });
  
  newRows = Object.values(newRows)
  let DataLen = newRows.length
  console.log(newRows.length)

  /*Nested for loop to find all timestamps*/
  for (let i = 0; i < DataLen; i++) {
    for (let j = 0; j < Data.length; j++)
    {
      if (Data[j]["timestamp"] == newRows[i]["timestamp"])
      {
        newRows[i][Data[j].name] = Number(Data[j].points)
      }
    }
  }
 
  if (newRows == undefined)
  {
    return null
  }
  return newRows
}
export let barcharts = null;
export function SortData(data)
{
  try{
     console.log(data)
  data = data.filter(item => !(item.FinishedPosition == 1 && item.Finaltime == "N/A"));
  // I need to make a constructors array which adds the drivers performances together
  let DriverBar = data

  /*Nested for loop to find all timestamps*/
  let points = 0;
  let TeamsArray = []
  for (let i = 0; i < data.length; i++) {
    points = points + data[i].points
    for (let j = 0; j < data.length; j++)
    {
      if (data[j].fullName == data[i].fullName && i != j)
      {
        points = points + data[j].points
      }
    }
    TeamsArray.push({teamname: data[i].fullName, points: points})
    points = 0
  }
  //This function filters out duplicats by comparing the name and points, not equal to index is ensuring we are not filting out the same index
  //We can now makae graphs with this data
  barcharts = TeamsArray.filter((item, index,arr) => arr.findIndex(i => i.teamname == item.teamname && i.points == item.points) != index);
  

  for (let i = DriverBar.length - 1; i > 0; i--) { 
    
    // Generate random index 
    const j = Math.floor(Math.random() * (i + 1));
                  
    // Swap elements at indices i and j
    const temp = DriverBar[i];
    DriverBar[i] = DriverBar[j];
    DriverBar[j] = temp;
  }
  DriverBar.sort(function(a,b){
      return b.points - a.points
    })
  if (DriverBar == undefined)
  {
    return null
  }
  return DriverBar
  }
  catch(error){
    throw new Error("Error");
  }
 
}