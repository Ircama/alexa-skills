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
		const speechText = 'Attendi che la diretta del Vaticano si attivi';
		return handlerInput.responseBuilder
			.speak(speechText)
			.addDirective({
                "type": "VideoApp.Launch",
                "videoItem": {
                  "source": "https://manifest.googlevideo.com/api/manifest/hls_playlist/expire/1586786825/ei/qR2UXtlBu4Lp2w_X05_YBw/ip/87.4.146.233/id/ojGaZWm93WU.1/itag/94/source/yt_live_broadcast/requiressl/yes/ratebypass/yes/live/1/goi/160/sgoap/gir%3Dyes%3Bitag%3D140/sgovp/gir%3Dyes%3Bitag%3D135/hls_chunk_host/r2---sn-uxaxpu5ap5-cbte.googlevideo.com/playlist_duration/30/manifest_duration/30/vprv/1/playlist_type/DVR/initcwndbps/4790/mh/nX/mm/44/mn/sn-uxaxpu5ap5-cbte/ms/lva/mv/m/mvi/1/pcm2cms/yes/pl/24/dover/11/keepalive/yes/fexp/23882513/mt/1586765176/disable_polymer/true/sparams/expire,ei,ip,id,itag,source,requiressl,ratebypass,live,goi,sgoap,sgovp,playlist_duration,manifest_duration,vprv,playlist_type/sig/AJpPlLswRAIgPSj9jTiFm_rHcvySBWdZQGdIF0C6k_x6MK70re7_jvQCIFucjgUFeP0evyUAjkYyEPP0iOQJdVDbxtoCnChOczZq/lsparams/hls_chunk_host,initcwndbps,mh,mm,mn,ms,mv,mvi,pcm2cms,pl/lsig/ALrAebAwRAIgSXc4syYoc5td6RXyfpF_nqdvb8MntNeMKWfelS_kis4CIGHaxwqcCcwzpWMv_vHB2F-O81r8UHhDQI12rO54FDzj/playlist/index.m3u8",
                  "metadata": {
                    "title": "Vaticano",
                    "subtitle": "Diretta del Vaticano"
                  }
                }
			})
			.getResponse();
	}
};

const StopIntentHandler = {
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
		const speechText = 'Grazie per aver guardato';
		return handlerInput.responseBuilder
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
		const speechText = 'Grazie per aver guardato';
		return handlerInput.responseBuilder
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
		const speechText = 'Grazie per aver guardato';
		return handlerInput.responseBuilder
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
			.getResponse();
	}
};

exports.handler = Alexa.SkillBuilders.custom()
	.addRequestHandlers(
		PlayHandler,
		StopIntentHandler,
		HelpIntentHandler,
		SessionEndedRequestHandler,
		IntentReflectorHandler)
	.addErrorHandlers(
		ErrorHandler)
	.lambda();
