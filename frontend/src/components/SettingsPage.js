import React from 'react'
import CreateRoomPage from './CreateRoomPage';
import { Grid, Button , Typography} from "@mui/material";
import { Link, useNavigate } from "react-router-dom"
function SettingsPage({Votes = 2 , CanPause = true, isHost=false , roomCode=null}){
    // const navigate = useNavigate()
    // if(!isHost || roomCode == null){
    //     navigate("/");
    // }
    return (
        <Grid container spacing={1} align="center">
            <Grid item xs={12}>
                <CreateRoomPage 
                    update={true} 
                    Votes={Votes} 
                    CanPause={CanPause}
                    roomCode={roomCode}
                    updateCallback={null}
                />
            </Grid>
        </Grid>
    )
}

export default SettingsPage