// placeholder for AJAX actions: registration, mock payment, map refresh
setInterval(async ()=>{
  const r = await fetch('/api/locations/');
  const locs = await r.json();
  // update map markers (implement as needed)
},15000);
