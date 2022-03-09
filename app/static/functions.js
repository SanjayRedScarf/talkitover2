
// Message seems to be a an object with attributes
// the send message function is called when the user send a new message
//(function () {
  var botResponseText = "";
  var sectionNumber = 1;
  var output = 1;
  var sentiment = 1;
  var initialHappinessValue = 0;
  var nextUserInput = "";
  //var currentUserInputIsFreeText = "false"; //need to initialise this based on whether the second implementation of the userinput div is actually free text or not
  //var currentUserInputIsOneToTen = "true";
  //var currentUserInputIsYesNo = "false";
  var initialHappinessValueSent = 0;
  var finalHappinessValue = 0;
  var finalHappinessValueSent = 0;
  var currentUserInputType = "initialHappinessSurvey"; // alternative values include: freeText and userInputButton
  var dataToStore = [];
  var anonymous = "true"
  var conversationId = "null"
  var botThinkingTime = 450;
  var userText = "";
  var Message;
  var message_side = "left";
  var sendDisabled = true;


  $( document ).ready(function() {
    window.history.replaceState({}, document.title, "/" + "");
  });

  // This is the message class
  Message = function (arg) {
      this.text = arg.text,
      this.message_side = arg.message_side;
      this.draw = function (_this) {
          return function () {
              var $message;
              $message = $($('.message_template').clone().html());
              $message.addClass(_this.message_side).find('.text').html(_this.text);
              $('.messages').append($message);
              return setTimeout(function () {
                  return $message.addClass('appeared');
              }, 0);
          };
      }(this);
      return this;
  };

  // this function appends the stop button to the chatbot window
  appendStopButton = function () {
    var stopButtonDiv = '<div id=stopButtonMarker class="stop_message"><div class="icon"></div><div class="text">stop</div></div>'
    $("#stopButtonholder").html(stopButtonDiv);
    $('.stop_message').click(function (e) {
        return initiateStopSection();
    });
  };

  // initiate the stop section
  initiateStopSection = function () {
    console.log("initiateStopSection() has been called");
    currentUserInputType = "stopButton";
    console.log("currentUserInputType is "+currentUserInputType);
    botMessage();
  }

  // print the message on the chatbot window
  printMessage = function (text, message_side) {
      var $messages, message;
      if (text.trim() === '') {
          return;
      }
      $messages = $('.messages');
      message = new Message({
          text: text,
          message_side: message_side
      });
      message.draw();
      $messages.animate({ scrollTop: $messages.prop('scrollHeight') }, 300);
      return
  };

  // remove the bots latest message
  removeLatestMessage = function(){
    $('.messages img:last-child').remove();
  }

  // add the bot thinking elipsis
  addBotThinking = function(time=0){
    var image;
    //var botThinkingHtml = '<img class="botText" src="https://raw.githubusercontent.com/SanjayRedScarf/talkitover2/SanjayRedScarf-new/typing_dots_cropped.gif" style="width:90px; height:40px; margin-bottom: 10px;"/>'
    var botThinkingHtml = '<img class="botText" src="/static/typing_dots_cropped_roundedcorners.gif" style="width:90px; height:50px; margin-bottom: 10px;"/>'
    var bot
    setTimeout(function(){
      $('.messages').append(botThinkingHtml);
      $('.messages').animate({ scrollTop: $('.messages').prop('scrollHeight') }, 300)
    }, time);
  }

  // print the bot message and add the html
  place_html_bind_functions = function (response, time, currentUserInputType="null", nextUserInput="null", add_html=false){
    setTimeout(function(){
      removeLatestMessage();
      printMessage(response, "left"); // print the message on the screen
      // add html and disable or enable buttons
      if (add_html==true){
        if (currentUserInputType=="freeText") {
          $(".message_input_wrapper").html(nextUserInput);
          bindEnterSend();
          $(".message_input").focus(); // click inside the textbox
        } else if (currentUserInputType == "initialHappinessSurvey"){
          $(".message_input_wrapper").html(nextUserInput);
          bindDropDown();
        } else if (currentUserInputType == "finalHappinessSurvey"){
          $(".message_input_wrapper").html(nextUserInput);
          bindDropDown();
        } else if (currentUserInputType == "userInputButton"){
          $(".message_input_wrapper").html(nextUserInput);
          bindDropDown();
        } else if (currentUserInputType == "stopButton"){
          $(".message_input_wrapper").html(nextUserInput);
          bindDropDown();
        }
      }
    }, time);
  };

  botMessage = function (message=""){

    userText = message;
    console.log("currentUserInputType = "+currentUserInputType);
    if (currentUserInputType=="freeText") {
    } else if (currentUserInputType == "initialHappinessSurvey"){
      //initialHappinessValue = $("#initialHappinessSurvey").val();
      initialHappinessValue = parseInt(userText, 10);
      //document.addEventListener('mouseout', mouseEvent);
    } else if (currentUserInputType == "finalHappinessSurvey"){
      //finalHappinessValue = $("#finalHappinessSurvey").val();
      finalHappinessValue = parseInt(userText, 10);
    } else if (currentUserInputType == "userInputButton"){
    } else if (currentUserInputType == "stopButton"){
      sectionNumber = 100; // the server will do the right thing if the section number is > 10, 100 is a randomly chosen number > 10
      userText = "stop";
      document.removeEventListener('mouseout', mouseEvent);} // the server will do the right thing if the user text is 'stop'
    console.log("userText has just been set as "+userText);
    $('.message_input').val('');

    //if the stop button has been pressed, we want to take the stop button away
    if(currentUserInputType=="stopButton"){$("#stopButtonMarker").remove();}

    if (initialHappinessValue>0){                         // if the initialHappinessValue has a value (i.e. if it's the first section)
      initialHappinessValueSent = initialHappinessValue;} // then the variable which sends the initialHappinessValue to the server (which we're calling initialHappinessValueSent) is set equal to that value
    else {initialHappinessValueSent = -1;}                // otherwise just give it a random value -- in this case -1 -- (otherwise it throws up an error about the int() function in python not accepting a nonetype)

    if (finalHappinessValue>0){                         // if the finalHappinessValue has a value (i.e. if it's the first section)
      finalHappinessValueSent = finalHappinessValue;}   // then the variable which sends the finalHappinessValue to the server (which we're calling finalHappinessValueSent) is set equal to that value
    else {finalHappinessValueSent = -1;}

    clientId = "bootstrapJavascriptClient"

    $.get("/get", { msg: JSON.stringify([userText, sectionNumber, output, initialHappinessValueSent, finalHappinessValueSent, anonymous, conversationId, clientId]) }).done(function(data) {
      var noOfResponseFragments = JSON.parse(data)[1];
      if (noOfResponseFragments == 1) {
        botResponseText = JSON.parse(data)[0];}
      else {
        var botResponseTextArray = JSON.parse(data)[0];
      }
      sectionNumber = JSON.parse(data)[2];
      nextUserInput = JSON.parse(data)[3];
      currentUserInputType = JSON.parse(data)[4];
      anonymous = JSON.parse(data)[5]
      conversationId = JSON.parse(data)[6]

      // This section generates the html for the things the bot says
      var botHtmlArray = [];
      if (noOfResponseFragments == 1){
        botHtmlArray[0] = botResponseText; // this is needed for the section which sets the botThinkingTime
      }
      else {
        //var responseFragment = 0; // This is for the for loop
        botHtmlArray = botResponseTextArray // This creates a string which consists of the bot's response together with the required html tags
      };

      // Determining the botThinkingTime
      if (currentUserInputType=="freeText") {       // if the user has just entered free text (as opposed to, e.g., some sort of dropdown or form)
        botThinkingTime = Math.max(userText.length*10,500); // set the thinking time to at least 500 milliseconds, and longer if the user text is long
        botThinkingTime = Math.min(botThinkingTime, 3000); // make sure the user doesn't have to wait more than 3 seconds for a response
      }

      botThinkingTimeBeforeSecondFragment = Math.min(1000+botHtmlArray[0].length*60,5000) // This website suggested that the formula should be timeToRead=1300+(chars∗65); (I made it a bit shorter than that)  https://psychology.stackexchange.com/questions/1147/how-long-does-it-take-to-read-a-sentence-with-x-number-of-characters
      if (sectionNumber == 12){
        document.addEventListener('mouseout', mouseEvent);
      };
      if (sectionNumber == 10){
        appendStopButton();
      };
      //delayPrint(botHtmlArray[0], botThinkingTime)
      //addBotThinking(200);
      if (botHtmlArray.length>1){
        place_html_bind_functions(botHtmlArray[0], botThinkingTime);
        addBotThinking(botThinkingTime+200);
        place_html_bind_functions(botHtmlArray[1], botThinkingTimeBeforeSecondFragment, currentUserInputType, nextUserInput, true);
      } else {
        place_html_bind_functions(botHtmlArray[0], botThinkingTime, currentUserInputType, nextUserInput, true);
      }
    });

  };

  // attach enter and send button to mainFunction function
  bindEnterSend = function(){
    $(document).ready(function(){
      $('.send_message').unbind().click(function (e) {
          return mainFunction();
      });
      $('.message_input').unbind().keypress(function (e) {
          if (e.which === 13) {
              return mainFunction();
          }
      });
    })
  }

  cleanUrl = function(){
    $( document ).ready(function() {
      window.history.replaceState({}, document.title, "/" + "my-new-url.html");
    });
  }

  // attach dropdown to mainFunction function
  bindDropDown = function(){
    $(document).ready(function(){
      $( ".message_input" ).unbind().change(function() {
        mainFunction();
      });
    });
  }

  // This function disables the send button when the user shouldn't be using it
  unbindAll = function(){
      $('.send_message').unbind();
      $('.message_input').unbind();
    };

  // This function retrieves the users message text
  getMessageText = function () {
      return $('.message_input').val();
  };
  function async_elipsis(){
    var image;
    //var botThinkingHtml = '<img class="botText" src="https://raw.githubusercontent.com/SanjayRedScarf/talkitover2/SanjayRedScarf-new/typing_dots_cropped.gif" style="width:90px; height:40px; margin-bottom: 10px;"/>'
    var botThinkingHtml = '<img class="botText" src="https://raw.githubusercontent.com/SanjayRedScarf/talkitover2/SanjayRedScarf-new/typing_dots_cropped_roundedcorners.gif" style="width:90px; height:50px; margin-bottom: 10px;"/>'
    var bot
    
    $('.messages').append(botThinkingHtml);
    $('.messages').animate({ scrollTop: $('.messages').prop('scrollHeight') }, 300);
    
  }
  let bot_promise = (message)=>{
    return new Promise((resolve,reject)=>{
      resolve(botMessage(message))
      reject(console.log('hello'))
    })
  }
  async function async_bot(message) {
    try{
      //async_elipsis();
      await bot_promise(message);
      async_elipsis();
    }
    catch{console.log('hello')}
    finally{console.log('hello')}

  }

  let eventListener;

  const show = () => {
    const element = document.querySelector("#popup");
    element.style.visibility = "visible";
    element.style.opacity = "1";
    element.style.transform = "scale(1)";
    element.style.transition = "0.4s, opacity 0.4s";
  
    eventListener = document.addEventListener("click", function (clickEvent) {
      let el = clickEvent.target;
      let inPopup = false;
      if (el.id === "popup") {
        inPopup = true;
      }
      while ((el = el.parentNode)) {
        if (el.id == "popup") {
          inPopup = true;
        }
      }
      if (!inPopup) hide();
    });
  };
  
  const hide = () => {
    const element = document.querySelector("#popup");
    element.style.visibility = "hidden";
    element.style.opacity = "0";
    element.style.transform = "scale(0.5)";
    element.style.transition = "0.2s, opacity 0.2s, visibility 0s 0.2s";
  
    if (eventListener) {
      document.removeEventListener(eventListener);
    }
  };
  
  const mouseEvent = e => {
    const shouldShowExitIntent = 
        !e.toElement && 
        !e.relatedTarget &&
        e.clientY < 10;

    if (shouldShowExitIntent) {
        document.removeEventListener('mouseout', mouseEvent);
        show();
    }
};

  // When the user hits send message then this funtion gets called
  mainFunction = function (){
    if ($(".message_input").val().replace(/\s/g, "").length > 0){
      unbindAll(true); // unbind all functions
      message = getMessageText();  // retrieve the users message text
      $(".message_input_wrapper").html("");
      printMessage(message, "right"); // display there message on the screen
      if (message =="stop"){
        
        initiateStopSection();
      } else {
        //async_elipsis();
        response = async_bot(message);
      };
    };
  };

(function () {
  $(function () {
    printMessage("Hi! I'm the Talk It Over chatbot and I am here for you to talk about whatever is on your mind. Thanks for trying this early prototype! I'm not a very clever piece of software and I might not understand everything you say, but if you think that talking things through in a safe confidential space might help, let's chat!", "left");
    addBotThinking();
    setTimeout(function () {
      var first_html = "" +
        "<select type='number' class='message_input' id='initialHappinessSurvey'> " +
        "<option selected disabled>Please select how you feel...</option>" +
        "<option name='initialHappinessValue' value=1>1</option>" +
        "<option name='initialHappinessValue' value=2>2</option>" +
        "<option name='initialHappinessValue' value=3>3</option>" +
        "<option name='initialHappinessValue' value=4>4</option>" +
        "<option name='initialHappinessValue' value=5>5</option>" +
        "<option name='initialHappinessValue' value=6>6</option>" +
        "<option name='initialHappinessValue' value=7>7</option>" +
        "<option name='initialHappinessValue' value=8>8</option>" +
        "<option name='initialHappinessValue' value=9>9</option>" +
        "<option name='initialHappinessValue' value=10>10</option>" +
        "</select>"
       removeLatestMessage();
       printMessage("To start, please rate how you feel on a scale from 1 to 10, where 1 is terrible and 10 is great", "left");
       $(".message_input_wrapper").html(first_html);
       $( ".message_input" ).unbind().change(function() {
             mainFunction();
           });
       //$(".message_input").focus();
    }, 3000);

  });
}.call(this));
