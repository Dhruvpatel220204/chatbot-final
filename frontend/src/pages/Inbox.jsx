import React, {useEffect, useState} from 'react';
import {Link} from 'react-router-dom';
import API from '../config';

export default function Inbox(){
  const [users, setUsers] = useState([]);
  const [q, setQ] = useState('');
  const token = localStorage.getItem('token');

  async function fetchUsers(){
    if(!token) return;
    const res = await fetch(`${API}/api/users?q=${encodeURIComponent(q)}`, {
      headers: {'Authorization': 'Bearer ' + token}
    });
    if(res.ok){
      const data = await res.json();
      setUsers(data);
    }
  }
  useEffect(()=>{ fetchUsers(); }, [q]);

  return (
    <div>
      <h3>Inbox</h3>
      <div style={{marginBottom:10}}>
        <input placeholder="Search users" value={q} onChange={e=>setQ(e.target.value)}/>
        <button onClick={fetchUsers}>Search</button>
      </div>
      <div>
        <h4>Quick: Chat with Bot</h4>
        <Link to={'/chat/' + encodeURIComponent('__bot__@whatsease')}>Open Bot Chat</Link>
      </div>
      <hr/>
      <div>
        <h4>Users</h4>
        {users.map(u=>(
          <div key={u.email} style={{padding:8, borderBottom:'1px solid #ddd'}}>
            <div><strong>{u.display_name || u.email}</strong></div>
            <div>{u.email}</div>
            <div><Link to={'/chat/' + encodeURIComponent(u.email)}>Chat</Link></div>
          </div>
        ))}
        {users.length===0 && <div>No users (or login to see users).</div>}
      </div>
    </div>
  );
}
