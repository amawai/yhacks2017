var config = {};

//Set the MongoDB connection variable
if (process.env.MONGO_CONNECT) 
{
    config.mongo_connect = process.env.MONGO_CONNECT;
    console.log("Local environment variable found, overriding global Mongo connection configuration...");
}
else {config.mongo_connect = "mongodb://testuser:testpassword@mongo-dev.local:27017/test?authSource=admin";}
//format environment variable in the same way as above.
//WARNING: this is might have to change with the release of MongoDB v3.6
//Mongoose might take care of it though (when it gets updated)...

//set the API route variable FOR TESTS
if (process.env.API_ROUTE)
{
    config.api_route = process.env.API_ROUTE;
    console.log("Local environment variable found, overriding global API route...")
}
else {config.api_route = "http://localhost:3000";}

config.token_password = "SuperMegaSecretThing";
config.user_token_password = "SuperMegaSecretThingForUsers";
config.password = "SuperSecretPasswordThatNobodyWillGuess";

module.exports = config;