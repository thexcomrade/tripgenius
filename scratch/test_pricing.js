function calculateHaversineDistance(lat1, lon1, lat2, lon2) {
  const R = 6371;
  const dLat = ((lat2 - lat1) * Math.PI) / 180;
  const dLon = ((lon2 - lon1) * Math.PI) / 180;
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos((lat1 * Math.PI) / 180) *
      Math.cos((lat2 * Math.PI) / 180) *
      Math.sin(dLon / 2) *
      Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return Math.round(R * c);
}

const tvm = { lat: 8.5241, lng: 76.9366 };
const ernakulam = { lat: 9.9816, lng: 76.2999 };
const varanasi = { lat: 25.3176, lng: 82.9739 };

const dErs = Math.round(calculateHaversineDistance(ernakulam.lat, ernakulam.lng, varanasi.lat, varanasi.lng) * 1.2);
const dTvm = Math.round(calculateHaversineDistance(tvm.lat, tvm.lng, varanasi.lat, varanasi.lng) * 1.2);

console.log('Ernakulam to Varanasi Distance:', dErs, 'km');
console.log('  Train Sleeper Min Fare: ₹' + Math.max(160, Math.round(dErs * 0.42)));
console.log('  Train 3AC Min Fare: ₹' + Math.max(540, Math.round(dErs * 1.05)));
console.log('  Flight Economy Approx: ₹6,500 - ₹9,500');

console.log('Trivandrum to Varanasi Distance:', dTvm, 'km');
console.log('  Train Sleeper Min Fare: ₹' + Math.max(160, Math.round(dTvm * 0.42)));
console.log('  Train 3AC Min Fare: ₹' + Math.max(540, Math.round(dTvm * 1.05)));
console.log('  Flight Economy Approx: ₹6,500 - ₹9,500');
