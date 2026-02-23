import {expect, assert} from 'chai'
import 'mocha'
import {CheckCookies,CheckIfLoginValid, CheckReg,WebSocketLibaryConnect} from '../src/Login_and_Register_functions.mjs';
import {setupServer} from 'msw/node';
import {http, HttpResponse,ws} from 'msw';

import sinon from 'sinon';


//http.get('/', ({ request, params, cookies }) => {})
//testing to see if we can mock responses
//const navigate = useNavigate();
 //ws.link("wss://localhost:82")


//Because we use sockets.io,
//we need to use sinon stubs for websockets.

sinon.stub()

const handlers = [
  http.post("http://localhost:82/CheckLogin", (req,res) => {
    return HttpResponse.json({
      status: 200,
      data: [{testdata : "We return data if status is correct"}]
  });
  }),
  http.post("http://localhost:82/CheckRegistration", (req,res) => {
    return HttpResponse.json({
      status: 200
  });
  }),
]



const testServer = setupServer(...handlers);


describe('Test if cookies comes back with a response', function()
{
  before(() => {
    testServer.listen({onUnhandledRequest: 'error'});
    
  })

  //Testing LoginPathway
  it("Testing Login", async function(){
    
    expect(await CheckIfLoginValid("np","np",null)).to.equal(200);    
  })
  //Testing Registration Pathway
  it ("Testing Registration", async function(){
    expect(await CheckReg("newusa","password","email","tele",null)).to.equal(200);    
  })
  
})

