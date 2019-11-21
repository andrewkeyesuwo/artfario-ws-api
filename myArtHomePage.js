exports.handler = async (event) => {
    var requestBody = JSON.parse(event.body);
    
    
    let imageInfo = {
        imageUrl: 'https://images.metmuseum.org/CRDImages/ep/original/DP367958.jpg',
        deckImageUrl: 'https://images.metmuseum.org/CRDImages/ep/original/DT1567.jpg'
    }

    if (requestBody) {
        if (requestBody.userID) {
            imageInfo.imageUrl = 'https://images.metmuseum.org/CRDImages/ad/original/12875.jpg'
        }    
    }
    
    const response = {
        headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': '*'
        },
        
        statusCode: 200,
        body: JSON.stringify(imageInfo)
    };
    return response;
};
