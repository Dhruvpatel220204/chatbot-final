import React, {useEffect, useState} from 'react';
import {useParams} from 'react-router-dom';
import API from '../config';

export default function ChatPage(){
  const { withEmail } = useParams();
  const decoded = decodeURIComponent(withEmail);
  const [messages, setMessages] = useState([]);
  const [text, setText] = useState('');
  const token = localStorage.getItem('token');
  const email = localStorage.getItem('email');

  async function fetchMessages(){
    if(!token) return;
    const res = await fetch(`${API}/api/messages?with=${encodeURIComponent(decoded)}`, {
      headers: {'Authorization':'Bearer ' + token}
    });
    if(res.ok){
      const data = await res.json();
      setMessages(data);
    }
  }

  // ...existing code...

async function handleDelete(id) {
  await fetch(`${API}/api/messages/${id}`, {
    method: 'DELETE',
    headers: {'Authorization':'Bearer ' + token}
  });
  fetchMessages();
}

async function send(){
  // ...existing send code...
}

// ...existing code...

return (
  <div>
    <h3>Chat with {decoded}</h3>
    <div style={{height:400, overflow:'auto', border:'1px solid #ccc', padding:10}}>
      {messages.map(m=>(
        <div key={m.message_id} style={{margin:8, textAlign: m.sender===email ? 'right' : 'left'}}>
          <div style={{display:'inline-block', padding:8, borderRadius:8, background: m.sender===email ? '#d1ffd6':'#f1f1f1' }}>
            <div>{m.content}</div>
            <div style={{fontSize:11, opacity:0.7}}>{new Date(m.timestamp).toLocaleString()}</div>
            {m.sender === email && (
              <button style={{marginLeft:8}} onClick={()=>handleDelete(m.message_id)}>Delete</button>
            )}
          </div>
        </div>
      ))}
    </div>
    <div style={{marginTop:10}}>
      <input value={text} onChange={e=>setText(e.target.value)} placeholder="Type message" style={{width:'80%'}}/>
      <button onClick={send}>Send</button>
    </div>
  </div>
);


  useEffect(()=>{
    fetchMessages();
    const id = setInterval(fetchMessages, 2000);
    return ()=> clearInterval(id);
  }, [withEmail]);

  async function send(){
    if(!text.trim()) return;
    const res = await fetch(`${API}/api/messages`, {
      method: 'POST',
      headers: {'Content-Type':'application/json', 'Authorization':'Bearer ' + token},
      body: JSON.stringify({recipient: decoded, content: text})
    });
    if(res.ok){
      setText('');
      fetchMessages();
    } else {
      alert('Send failed');
    }
  }

  return (
    <div>
      <h3>Chat with {decoded}</h3>
      <div style={{height:400, overflow:'auto', border:'1px solid #ccc', padding:10}}>
        {messages.map(m=>(
          <div key={m.message_id} style={{margin:8, textAlign: m.sender===email ? 'right' : 'left'}}>
            <div style={{display:'inline-block', padding:8, borderRadius:8, background: m.sender===email ? '#d1ffd6':'#f1f1f1' }}>
              <div>{m.content}</div>
              <div style={{fontSize:11, opacity:0.7}}>{new Date(m.timestamp).toLocaleString()}</div>
            </div>
          </div>
        ))}
      </div>
      <div style={{marginTop:10}}>
        <input value={text} onChange={e=>setText(e.target.value)} placeholder="Type message" style={{width:'80%'}}/>
        <button onClick={send}>Send</button>
      </div>
    </div>
  );
}
