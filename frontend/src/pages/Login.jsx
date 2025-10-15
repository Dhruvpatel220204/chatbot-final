import React, {useState} from 'react';
import {useNavigate} from 'react-router-dom';
import API from '../config';

export default function Login(){
  const [email,setEmail] = useState('');
  const [password,setPassword] = useState('');
  const [err,setErr] = useState('');
  const nav = useNavigate();

  async function submit(e){
    e.preventDefault();
    setErr('');
    try{
      const res = await fetch(`${API}/api/auth/login`, {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({email, password})
      });
      const data = await res.json();
      if(!res.ok){ setErr(data.error || 'Login failed'); return; }
      localStorage.setItem('token', data.access_token);
      localStorage.setItem('email', data.email);
      nav('/');
    }catch(err){
      setErr('Network error');
    }
  }

  return (
    <div>
      <h3>Login</h3>
      <form onSubmit={submit}>
        <div><input placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} required/></div>
        <div><input placeholder="Password" type="password" value={password} onChange={e=>setPassword(e.target.value)} required/></div>
        <div><button type="submit">Login</button></div>
        {err && <div style={{color:'red'}}>{err}</div>}
      </form>
    </div>
  );
}
