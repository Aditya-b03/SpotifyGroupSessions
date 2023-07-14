import React, { useState } from 'react';
import {TextField , Grid , Button , Typography } from "@mui/material"
import { Link , useNavigate } from 'react-router-dom';
function RoomJoinPage() {
  const navigate = useNavigate()
  const [State,SetState] = useState({
    roomCode : "",
    err : "",
  })

  const handleState = (e) => {
    SetState({
      roomCode : e.target.value,
      err : State.err
    })
  }

  const handlejoin = () => {
    const RequestOption = {
      method: "POST",
      headers: {"Content-Type" : "application/json"},
      body: JSON.stringify({
        code: State.roomCode
      }),
    }; 

    fetch('/api/join-room' , RequestOption).then((r) => {
      if(r.ok){
        navigate(`/Room/${State.roomCode}`)
      }else{
        SetState({
          err : `Room Not Found : ${State.roomCode}`,
          roomCode : "",
        })
      }
    }).catch((err) => {
      console.log(err);
    });
  }

  return (
      <Grid container rowSpacing={2} columnSpacing={1} align='center' bgcolor={'white'}>
        <Grid item xs={12}>
          <Typography component='h4' variant='h4'>
            Join a Room...
          </Typography>
        </Grid>
        <Grid item xs={12}>
          <TextField
            variant='outlined' 
            error={State.error} 
            label="code"
            placeholder='Enter Room Code' 
            helperText={State.err}
            value={State.roomCode}
            onChange={handleState}
            />
        </Grid>
        <Grid item xs={6} align='right'>
          <Button variant='contained' color='primary' onClick={handlejoin}> Join </Button>
        </Grid>
        <Grid item xs={6} align='left'>
          <Button variant='outlined' color='secondary' to='/' component={Link}>Back</Button>
        </Grid>
      </Grid>
  );
}

export default RoomJoinPage