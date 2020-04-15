# -*- coding: utf-8 -*-

import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.interfaces.videoapp import LaunchDirective, VideoItem, Metadata
from ask_sdk_model.interfaces.audioplayer import (
    PlayDirective, PlayBehavior, AudioItem, Stream, AudioItemMetadata,
    StopDirective)
from ask_sdk_model.interfaces import display
from ask_sdk_model import Response

from pytube import YouTube
import urllib.request, json
from urllib.error import  URLError, HTTPError

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (handler_input) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (handler_input) -> Response
        
        logger.info(">>>>> In LaunchRequestHandler")
        interfaces = (ask_utils.request_util
            .get_supported_interfaces(handler_input)
            .to_dict())

        with open("parameters.json") as conf_data:
            conf = json.load(conf_data)
        locale = ask_utils.get_locale(handler_input)
        logger.debug(f"Locale is {locale}")
        # localized strings stored in language_strings.json
        with open("language_strings.json") as language_prompts:
            language_data = json.load(language_prompts)
        try:
            loc_data = language_data[locale[:2]]
            skill_name = loc_data['SKILL_NAME']
        except KeyError:
            loc_data = language_data['en']
            skill_name = loc_data['SKILL_NAME']
        speak_output = loc_data['NO_VIDEO']
        channel_id = loc_data['CHANNEL']
        youtube_url = (
            "https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=" +
            channel_id +
            "&maxResults=1&order=date&type=video&key=" +
            conf['youtube_key']
        )
        success = True
        try:
            url = urllib.request.urlopen(youtube_url)
        except URLError as e:
            speak_output = loc_data['URL_ERROR']
            logger.info("URLError %s", e)
            success = False
        except HTTPError as e:
            logger.info("HTTPError %s, %e", e, e.code)
            if e.code == 429:
                speak_output = loc_data['TOO_MANY_REQUESTS']
            success = False
        if success:
            try:
                data = json.loads(url.read().decode())
                videoId = data['items'][0]['id']['videoId']
                yt = YouTube('https://www.youtube.com/watch?v=' + videoId)
            except Exception as e:
                speak_output = loc_data['YOUTUBE_ERROR']
                success = False
        if success:
            logger.info("List of the available interfaces: %s", interfaces)
            if interfaces['video_app'] is not None: # device has video support
                for stream in yt.streams.order_by('resolution').desc():
                    if stream.includes_audio_track:
                        break
                speak_output = loc_data['VIDEO_MESSAGE'] + ": " + stream.title + ". " + yt.description
                logger.info("Video {}. "
                            "Locale='{}'. "
                            "channel_id='{}'. "
                            "speak_output='{}'. "
                            "youtube_key='{}'".format(
                    stream,
                    locale[:2],
                    channel_id,
                    speak_output,
                    conf['youtube_key'])
                )
                directive = LaunchDirective(video_item=VideoItem(
                    source=stream.url,
                    metadata=Metadata(title=stream.title, subtitle=yt.description)))
                return (
                    handler_input.response_builder
                        .speak(speak_output)
                        .add_directive(directive)
                        .response
                )
            elif interfaces['audio_player'] is not None: # device has only audio support (no video)
                stream = (yt.streams
                            .filter(only_audio=True, subtype='mp4')
                            .order_by('fps')
                            .desc()
                            .first()
                )
                speak_output = loc_data['AUDIO_MESSAGE'] + ": " + stream.title + ". " + yt.description
                logger.info("Audio {}. "
                            "Locale='{}'. "
                            "channel_id='{}'. "
                            "speak_output='{}'. "
                            "youtube_key='{}'".format(
                    stream,
                    locale[:2],
                    channel_id,
                    speak_output,
                    conf['youtube_key'])
                )
                directive = PlayDirective(
                    play_behavior=PlayBehavior.REPLACE_ALL,
                    audio_item=AudioItem(
                        stream=Stream(
                            expected_previous_token=None,
                            token=stream.url,
                            url=stream.url,
                            offset_in_milliseconds=0
                        ),
                        metadata=AudioItemMetadata(
                            title=stream.title,
                            subtitle=yt.description,
                            art=display.Image(
                                content_description=stream.title,
                                sources=[
                                    display.ImageInstance(
                                        url=yt.thumbnail_url
                                    )
                                ]
                            ),
                            background_image=display.Image(
                                content_description=stream.title,
                                sources=[
                                    display.ImageInstance(
                                        url=yt.thumbnail_url
                                    )
                                ]
                            )
                        )
                    )
                )
                return (
                    handler_input.response_builder
                        .speak(speak_output)
                        .add_directive(directive)
                        .set_should_end_session(True)
                        .response
                )
            else:
                speak_output = loc_data['NO_INTERFACE'] + ": " + stream.title + ". " + yt.description
        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class MainIntentHandler(AbstractRequestHandler):
    """Handler for Main Intent."""
    def can_handle(self, handler_input):
        # type: (handler_input) -> bool
        return (ask_utils.is_intent_name("mainIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.ResumeIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.NavigateHomeIntent")(handler_input))

    def handle(self, handler_input):
        # type: (handler_input) -> Response
        logger.info(">>>>> In MainIntentHandler: %s", handler_input.request_envelope.request)
        speak_output = "No main intent implemented"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (handler_input) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (handler_input) -> Response
        logger.info(">>>>> In HelpIntentHandler")
        speak_output = "No help intent implemented"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class AudioPlaybackHandler(AbstractRequestHandler):
    """Handler for audio playback events."""
    def can_handle(self, handler_input):
        # type: (handler_input) -> bool
        return (ask_utils.is_request_type("AudioPlayer.PlaybackStarted")(handler_input) or
                ask_utils.is_request_type("AudioPlayer.PlaybackFinished")(handler_input) or
                ask_utils.is_request_type("AudioPlayer.PlaybackStopped")(handler_input) or
                ask_utils.is_request_type("AudioPlayer.PlaybackNearlyFinished")(handler_input) or
                ask_utils.is_request_type("AudioPlayer.PlaybackFailed")(handler_input))

    def handle(self, handler_input):
        # type: (handler_input) -> Response
        logger.debug(">>>>> In AudioPlaybackHandler")
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (handler_input) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.PauseIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (handler_input) -> Response

        logger.info(">>>>> In CancelOrStopIntentHandler")
        locale = ask_utils.get_locale(handler_input)
        with open("language_strings.json") as language_prompts:
            language_data = json.load(language_prompts)
        try:
            loc_data = language_data[locale[:2]]
            skill_name = loc_data['SKILL_NAME']
        except KeyError:
            loc_data = language_data['en']
            skill_name = loc_data['SKILL_NAME']
        speak_output = loc_data['GOODBYE']
        directive = StopDirective()

        return (
            handler_input.response_builder
                .speak(speak_output)
                .add_directive(directive)
                .set_should_end_session(True)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (handler_input) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (handler_input) -> Response

        logger.info(">>>>> In SessionEndedRequestHandler")
        logger.debug("Session ended with reason: {}".format(
            handler_input.request_envelope.request.reason)
        )
        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (handler_input) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (handler_input) -> Response

        logger.info(">>>>> In IntentReflectorHandler")
        intent_name = ask_utils.get_intent_name(handler_input)
        logger.info("Triggered intent: %s", intent_name)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (handler_input, exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (handler_input, exception) -> Response

        logger.info(">>>>> In CatchAllExceptionHandler: check handler '%s'",
            ask_utils.get_request_type(handler_input)
        )
        logger.debug("Dump of request_envelope: %s",
            str(handler_input.request_envelope)
        )
        logger.error(exception, exc_info=True)

        return handler_input.response_builder.response

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(MainIntentHandler())
sb.add_request_handler(AudioPlaybackHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
