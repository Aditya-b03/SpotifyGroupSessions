import React from 'react';
import { Grid , Typography , Card , IconButton , LinearProgress } from '@mui/material';
import {PlayCircleFilledWhite , SkipNext , Pause} from '@mui/icons-material'
const Player = (props) => {

    const songProgress = (props.time/props.duration)*100

    const HandlePause = () => {
        const RO = {
            method : "PUT",
            headers : { "Content-type": "application/json"}
        };
        fetch("/spotify/pause" , RO);
    }

    const HandlePlay = () => {
        const RO = {
            method : "PUT",
            headers : { "Content-type": "application/json"}
        };
        fetch("/spotify/play" , RO);
    }


  return (
    <Card raised={true}>
        <Grid container alignItems='center'>
            <Grid item xs={4} align="center">
                <img src={props.cover_url} width="100%" height="100%"/>
            </Grid>
            <Grid item xs={8} align="center">
                <Typography component="h5" variant='h5'>
                    {props.title}
                </Typography>
                <Typography color='textSecondary' variant='h5'>
                    {props.artist}
                </Typography>
                <div>
                    <IconButton onClick={()=>{
                        return props.is_playing ? HandlePause() : HandlePlay();
                    }}>
                        {props.is_playing ? <Pause/> : <PlayCircleFilledWhite/>}
                    </IconButton>
                    <IconButton>
                        <SkipNext />
                    </IconButton>
                </div>
            </Grid>
        </Grid>
        <LinearProgress variant='determinate' value={songProgress}/>
    </Card>
  )
}

export default Player