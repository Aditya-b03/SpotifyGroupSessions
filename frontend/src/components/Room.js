import React, { useEffect } from "react";
import { useState, } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { Grid, Button , Typography} from "@mui/material";
import { Routes , Route , Link} from "react-router-dom";
import SettingsPage from "./SettingsPage";
import Player from "./player";
import { blueGrey } from "@mui/material/colors";
function Room(props){
    const navigate = useNavigate();
    // useParams hookmto access url parameters 
    const roomCode = useParams().roomCode;
    const [currentSong , SetCurrentSong] = useState({})
    const [State,SetState] = useState({
        Votes : 2,
        CanPause : false,
        isHost : false,
        is_Auth : false,
    })

    const Auth_spotity = ()=>{
        console.log("Auth...")
        //check if already auth
        fetch('/spotify/is-auth')
        .then((r) => r.json())
        .then((d) => {
            SetState({
                ...State,
                isHost : true,
                is_Auth : d.status,
            });
            // if not already auth
            if(!d.status){
                // fetch the redirect url for auth
                fetch('/spotify/get-auth-url')
                .then((r) => r.json())
                .then((d) => {
                    window.location.replace(d.url);
                });
            }
        });
    }

    const getCurrentsong = () => {
        fetch('/spotify/current-song').then((r)=>{
            if(!r.ok){
                return {};
            }
            else{
                return r.json();
            }
        }).then((d) => {
            SetCurrentSong(d);
            //console.log(d);
        });
    }

    useEffect(() => {
        fetch('/api/get-room' + '?code=' + roomCode).then((r) => {
            if(!r.ok){
                props.leaveRoomCallback();
                navigate("/");
            }
            return r.json()
        }).then((d)=>{
            SetState({
                Votes : d.votes_to_skip,
                CanPause : d.guest_can_pause,
                isHost : d.is_host,
                is_Auth : false,
            });
            if(d.is_host){
                Auth_spotity();
            }
        });
    },[roomCode]);

    useEffect(()=> {
        const interval = setInterval(getCurrentsong , 1000);
        return () => { 
            clearInterval(interval);
        };
    },[])

    const LeaveRoomhandler = () =>{
        const RO = {
            method : "POST",
            headers : { "Content-type": "application/json"}
        };
        fetch("/api/leave-room",RO).then((r) =>{
            props.leaveRoomCallback();
            navigate("/");
        });
    }

    const renderSettingButton = () => {
       return  (<Grid item xs={12} >
        <Button color="primary" to={"/Room/" +roomCode+ "/Settings"} component={Link}>Settings</Button>
    </Grid>)
    }

    function renderRoom(){
        return  (
            <Grid container spacing={1} align="center" bgcolor={blueGrey}>
                <Grid item xs={12} >
                    <Typography variant="h4" component="h4">
                        Code : {roomCode}
                    </Typography>
                </Grid>
                <Grid item xs={12}>
                <div className="player" >
                    <Player {...currentSong}></Player>
                </div>
                </Grid>
                {State.isHost ? renderSettingButton() : null}
                <Grid item xs={12} >
                    <Button variant="contianed" onClick={LeaveRoomhandler} >Leave Room</Button>
                </Grid>
            </Grid>
            );
    }
    
    // Colon in url represent a variable of some kind in url
    return (
        
        <Routes>
            <Route path="/" element={renderRoom()}/>
            <Route 
                path="/Settings" 
                element={<SettingsPage 
                            roomCode={roomCode} 
                            Votes={State.Votes} 
                            CanPause={State.CanPause} 
                            isHost={State.isHost} 
                />}
            />
        </Routes>
        
    );
}
export default Room;
/* 
<div>
    <h3>Room Code : {roomCode}</h3>
    <p><b>Votes to Skip</b> : {State.Votes}</p>
    <p><b>Guest can pause</b> : {State.CanPause.toString()}</p>
    <p><b>Host</b> : {State.isHost.toString()}</p>
</div>
*/