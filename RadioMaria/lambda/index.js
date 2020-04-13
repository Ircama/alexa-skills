const Alexa = require('ask-sdk-core');
var https = require('https');

const PlayHandler = {
	canHandle(handlerInput)
	{
		return (
			handlerInput.requestEnvelope.request.type === 'LaunchRequest' ||
			(
				handlerInput.requestEnvelope.request.type === 'IntentRequest' &&
				handlerInput.requestEnvelope.request.intent.name === 'Play'
			) ||
			(
				handlerInput.requestEnvelope.request.type === 'IntentRequest' &&
				handlerInput.requestEnvelope.request.intent.name === 'AMAZON.ResumeIntent'
			)
		);
	},
	handle(handlerInput)
	{
		return handlerInput.responseBuilder
			.addDirective({
				type: 'AudioPlayer.Play',
				playBehavior: 'REPLACE_ALL',
				audioItem:{
					stream:{
						token: '0',
						url: 'https://dreamsiteradiocp5.com/proxy/rmitalia?mp=/stream',
						offsetInMilliseconds: 0
					},
					metadata:{
					    title: 'Riproduzione in diretta di Radio Maria Italia',
					    subtitle: 'Pronuncia "Alexa Stop" per interrompere',
                        art: {
                          contentDescription:"RadioMariaTitle",
                          sources: [{
                            url:"https://www.radiomaria.org/wp-content/themes/portale/images/santaLina.png"
                          }]
                        }
					}
				}
			})
			.getResponse();
	}
};

const PauseStopHandler = {
	canHandle(handlerInput)
	{
		return (
				handlerInput.requestEnvelope.request.type === 'IntentRequest' &&
				(
					handlerInput.requestEnvelope.request.intent.name === 'AMAZON.CancelIntent' ||
					handlerInput.requestEnvelope.request.intent.name === 'AMAZON.StopIntent'
				)
			) ||
			(
				handlerInput.requestEnvelope.request.type === 'IntentRequest' &&
				handlerInput.requestEnvelope.request.intent.name === 'AMAZON.PauseIntent'
			);
	},
	handle(handlerInput)
	{
		const speechText = 'Grazie per aver ascoltato Radio maria';
		return handlerInput.responseBuilder
			.addDirective({
				type: 'AudioPlayer.Stop',
				clearBehavior: 'CLEAR_ALL'
			})
			.speak(speechText)
			.withShouldEndSession(true)
			.getResponse();
	}
};

const HelpIntentHandler = {
	canHandle(handlerInput)
	{
		return handlerInput.requestEnvelope.request.type === 'IntentRequest' &&
			handlerInput.requestEnvelope.request.intent.name === 'AMAZON.HelpIntent';
	},
	handle(handlerInput)
	{
		const speechText = 'Grazie per aver ascoltato Radio maria';
		return handlerInput.responseBuilder
			.addDirective({
				type: 'AudioPlayer.Stop',
				clearBehavior: 'CLEAR_ALL'
			})
			.speak(speechText)
			.withShouldEndSession(true)
			.getResponse();
	}
};

const SessionEndedRequestHandler = {
	canHandle(handlerInput)
	{
		return handlerInput.requestEnvelope.request.type === 'SessionEndedRequest';
	},
	handle(handlerInput)
	{
		const speechText = 'Grazie per aver ascoltato Radio maria';
		return handlerInput.responseBuilder
			.addDirective({
				type: 'AudioPlayer.Stop',
				clearBehavior: 'CLEAR_ALL'
			})
			.speak(speechText)
			.withShouldEndSession(true)
			.getResponse();
	}
};

const IntentReflectorHandler = {
	canHandle(handlerInput)
	{
		return handlerInput.requestEnvelope.request.type === 'IntentRequest';
	},
	handle(handlerInput)
	{
		const intentName = handlerInput.requestEnvelope.request.intent.name;
		const speechText = "nessun testo di aiuto per l'intento";
		return handlerInput.responseBuilder
			.speak(speechText)
			.withShouldEndSession(true)
			.getResponse();
	}
};

const ErrorHandler = {
	canHandle()
	{
		return true;
	},
	handle(handlerInput, error)
	{
		const speechText = `Mi spiace, non ho capito quello che hai detto. Puoi ripetere?`;
		return handlerInput.responseBuilder
			.speak(speechText)
			.reprompt(speechText)
			.addDirective({
				type: 'AudioPlayer.Stop',
				clearBehavior: 'CLEAR_ALL'
			})
			.getResponse();
	}
};

exports.handler = Alexa.SkillBuilders.custom()
	.addRequestHandlers(
		PlayHandler,
		PauseStopHandler,
		HelpIntentHandler,
		SessionEndedRequestHandler,
		IntentReflectorHandler)
	.addErrorHandlers(
		ErrorHandler)
	.lambda();