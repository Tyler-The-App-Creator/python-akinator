const api = require('akinator-api');

api.start('US', (gameData, error)=>{
	if (error) {
		console.log(error);
	} else {
		console.log(gameData);
	}
})
