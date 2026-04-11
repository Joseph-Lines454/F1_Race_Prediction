
export let DriverColoursGraph = {}
export function AssignDriverColours(DriversLen, Drivers){
  //Random colours function
  let array = []
  console.log(DriversLen)
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
 
  return newRows
}