import React from 'react'
import Button from "@mui/material/Button"
import Grid from "@mui/material/Grid"
import Typography  from '@mui/material/Typography'
import { TextField } from '@mui/material'
import FormHelperText from '@mui/material/FormHelperText'
import FormControlLabel from '@mui/material/FormControlLabel'
import FormControl from '@mui/material/FormControl'
import { Link } from "react-router-dom"
import  Radio from "@mui/material/Radio" 
import RadioGroup from "@mui/material/RadioGroup"
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Collapse } from '@mui/material'


/*
--> Update CallBack Remaining to implement
*/
const CreateRoomPage = ({Votes = 2 , CanPause = true, update = false, roomCode = null, updateCallBack=()=>{},}) => {

  // Hook instead of UseHistory for navigating to a different page
  const navigate = useNavigate();

  var default_votes = 2
  const [State , SetState] = useState({
    Votes : Votes,
    CanPause : CanPause,
    SuccessMsg : "",
    ErrorMsg : "",
  });
  const handleVotesChange = (e) => {
    //console.log(State)
    SetState({
      ...State,
      Votes : e.target.value
    })
  }
  
  const handleCanPause = (e) => {
    //console.log(State)
    SetState({
      ...State,
      CanPause : e.target.value
    })
  }

  const handleCreate = () => {
    //console.log(State);
    const RequestOption = {
      method: "POST",
      headers: {"Content-Type" : "application/json"},
      body: JSON.stringify({
        votes_to_skip : State.Votes,
        guest_can_pause : State.CanPause,
      }),
    };

    // whatever fetch gets back is the goes to r , whatever r.json() return goes to d
    // history -> useHistory -> useNavigate , for update version of reactRouterDom
    fetch("/api/create-room" , RequestOption).then((r) =>
        r.json()
      ).then((d) => 
        navigate('/Room/' + d.code)
        );
  }

  const handleUpdate=()=>{
    //console.log(State);
    const RequestOption = {
      method: "PATCH",
      headers: {"Content-Type" : "application/json"},
      body: JSON.stringify({
        votes_to_skip : State.Votes,
        guest_can_pause : State.CanPause,
        code : roomCode,
      }),
    };

    fetch("/api/update-room" , RequestOption).then((r) =>{
      if(r.ok){
        SetState({
          ...State,
          SuccessMsg : "Room Updated Successfully!"
        })
      }else{
        SetState({
          ...State,
          ErrorMsg : "Error while updating!"
        })
      }
    });
  }

  //render params
  const title = update ? "Update Your Room..." : "Create Your Own Room...";
  const buttontitle = update ? "Update" : "Create";

  return (
    // Spacing between the items in the grid : 1 = 8px
    //xs={12} sizes a component to occupy the whole viewport width regardless of its size.
    <Grid container spacing={1} bgcolor={"white"} borderRadius={10} align="center">
      <Grid item xs={12} align="center">
        <Collapse in={State.SuccessMsg != "" || State.ErrorMsgMsg != ""}>
          {State.SuccessMsg}
        </Collapse>
      </Grid>
      <Grid item xs={12} align="center">
        <Typography component='h4' variant='h4'>
          {title}
        </Typography>
      </Grid>
      <Grid item xs={12} align="center">
        <FormControl component="fieldset">
          <FormHelperText component="div">
            <div align='center'>
              Guest Control of Playback state
            </div>
          </FormHelperText>
          <RadioGroup onChange={handleCanPause} row defaultValue={CanPause.toString()}>
            <FormControlLabel 
              value="true"
              control={<Radio color="primary" />}
              label="Play/Pause"
              labelPlacement="bottom"
              />
            <FormControlLabel 
              value="false"
              control={<Radio color="secondary" />}
              label="No Control"
              labelPlacement="bottom"
              />
            </RadioGroup>
            <Grid item xs={12} align="center">
              <TextField onChange={handleVotesChange}required={true} defaultValue={State.Votes}  type="number" inputProps={{
                min : 1,
                style : { textAlign: "center"}
              }}/>
              <FormHelperText component="div"><div align="center">Voter to Skip</div></FormHelperText>
            </Grid>
        </FormControl>
      </Grid>
      <Grid item xs={6} align="right">
        <Button onClick={() => {
          return update ? handleUpdate():handleCreate()}} color='primary' variant="contained">{buttontitle}</Button>
      </Grid>
      <Grid item xs={6} align="left">
        <Button color='secondary' variant="outlined" to="/" component={Link}>Back</Button>
      </Grid>
    </Grid>
  ) 
}

export default CreateRoomPage