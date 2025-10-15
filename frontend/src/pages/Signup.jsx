import React, {useState} from 'react';
import {useNavigate} from 'react-router-dom';
import API from '../config';

export default function Signup(){
  const [email,setEmail] = useState('');
  const [password,setPassword] = useState('');
  const [display,setDisplay] = useState('');
  const [err,setErr] = useState('');
  const nav = useNavigate();

  async function submit(e){
    e.preventDefault();
    setErr('');
    try{
      const res = await fetch(`${API}/api/auth/signup`, {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({email, password, display_name: display})
      });
      const data = await res.json();
      if(!res.ok){ setErr(data.error || 'Signup failed'); return; }
      alert('Created. Please login.');
      nav('/login');
    }catch(err){
      setErr('Network error');
    }
  }

  return (
    <div>
      <h3>Signup</h3>
      <form onSubmit={submit}>
        <div><input placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} required/></div>
        <div><input placeholder="Display name" value={display} onChange={e=>setDisplay(e.target.value)} /></div>
        <div><input placeholder="Password" type="password" value={password} onChange={e=>setPassword(e.target.value)} required/></div>
        <div><button type="submit">Signup</button></div>
        {err && <div style={{color:'red'}}>{err}</div>}
      </form>
    </div>
  );
}
