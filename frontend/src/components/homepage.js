import React, { useState } from "react";
import { BrowserRouter as Router , Routes , Route , Link , Navigate} from "react-router-dom";
import CreateRoomPage from "./CreateRoomPage";
import RoomJoinPage from "./RoomJoinPage";
import Room from "./Room";
import { Button, ButtonGroup, Typography , Grid } from "@mui/material";
function Homepage(){
    const [roomCode,SetRoomcode] = useState(null);
    async function componentDidMount(){
        try {
            const r = await fetch('/api/user-in-room')
            const d = await r.json()
            SetRoomcode(d.code);
        }
        catch(err){
            console.log("ERROR!")
            console.log(err);
        }
    }

    componentDidMount()


    const clearRoomCode = () => {
        console.log("Clearing room code", roomCode);
        SetRoomcode(null);
        console.log(roomCode)
    }

    function renderHomepage(){
        
        return (
                <Grid container spacing={3} align="center">
                    <Grid item xs={12}>
                        <Typography variant="h3" compact='h3'>
                            House Party
                        </Typography>
                    </Grid>
                    <Grid item xs={12}>
                        <ButtonGroup variant="contained">
                            <Button color="primary" to="/join" component={Link}>Join a Room</Button>
                            <Button color="secondary" to='/create' component={Link}>Create Own Room</Button>
                        </ButtonGroup>
                    </Grid>
                </Grid>
            )
        
    };

    // Colon in url represent a variable of some kind in url
    return (
        <Router>
            <Routes>
                <Route exact path="/" element={
                    roomCode ? (<Navigate to={`/Room/${roomCode}`} replace={true} />) : renderHomepage()
                    }/>
                <Route path="/join" element={<RoomJoinPage/>}/>
                <Route path="/create" element={<CreateRoomPage/>}/>
                <Route path="/Room/:roomCode/*" element={<Room leaveRoomCallback={clearRoomCode} />}/>
            </Routes>
        </Router>
    );
}



export default Homepage;
