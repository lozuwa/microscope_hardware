package me.yogeshwardan.mqttsubscriber;

import android.app.Activity;
import android.content.Intent;
import android.net.Uri;
import android.os.Environment;
import android.provider.MediaStore;
import android.support.v4.content.FileProvider;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.ImageView;
import android.widget.Toast;

import org.eclipse.paho.android.service.MqttAndroidClient;
import org.eclipse.paho.client.mqttv3.IMqttActionListener;
import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.IMqttToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;

import java.io.File;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;

public class MainActivity extends AppCompatActivity implements MqttCallback{

    /**********************************MQTT***************************************************/

    private static final String TAG = "MainActivity";
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        //MQTTConnect options : setting version to MQTT 3.1.1
        //MqttConnectOptions options = new MqttConnectOptions();
        //options.setMqttVersion(MqttConnectOptions.MQTT_VERSION_3_1);
        //options.setUserName("your_mqtt_username_here");
        //options.setPassword("your_mqtt_password_here".toCharArray());

        //Below code binds MainActivity to Paho Android Service via provided MqttAndroidClient
        // client interface
        //Todo : Check why it wasn't connecting to test.mosquitto.org. Isn't that a public broker.
        //Todo : .check why client.subscribe was throwing NullPointerException  even on doing subToken.waitForCompletion()  for Async                  connection estabishment. and why it worked on subscribing from within client.connect’s onSuccess(). SO
        String clientId = MqttClient.generateClientId();
        final MqttAndroidClient client =
                new MqttAndroidClient(this.getApplicationContext(), "tcp://test.mosquitto.org:1883", clientId);

        try {
            IMqttToken token = client.connect();
            token.setActionCallback(new IMqttActionListener() {
                @Override
                public void onSuccess(IMqttToken asyncActionToken) {
                    // We are connected
                    Log.d(TAG, "onSuccess");
                    Toast.makeText(MainActivity.this, "Connection successful", Toast.LENGTH_SHORT).show();
                    //Subscribing to a topic door/status on broker.hivemq.com
                    client.setCallback(MainActivity.this);
                    final String topic = "/test";
                    int qos = 1;
                    try {
                        IMqttToken subToken = client.subscribe(topic, qos);
                        subToken.setActionCallback(new IMqttActionListener() {
                            @Override
                            public void onSuccess(IMqttToken asyncActionToken){
                                // successfully subscribed
                                Toast.makeText(MainActivity.this, "Successfully subscribed to: " + topic, Toast.LENGTH_SHORT).show();
                            }

                            @Override
                            public void onFailure(IMqttToken asyncActionToken,
                                                  Throwable exception) {
                                // The subscription could not be performed, maybe the user was not
                                // authorized to subscribe on the specified topic e.g. using wildcards
                                Toast.makeText(MainActivity.this, "Couldn't subscribe to: " + topic, Toast.LENGTH_SHORT).show();

                            }
                        });
                    } catch (MqttException e) {
                        e.printStackTrace();
                    } catch (NullPointerException e) {
                        e.printStackTrace();
                    }
                }

                @Override
                public void onFailure(IMqttToken asyncActionToken, Throwable exception) {
                    // Something went wrong e.g. connection timeout or firewall problems
                    Log.d(TAG, "onFailure");
                    Toast.makeText(MainActivity.this, "Connection failed", Toast.LENGTH_SHORT).show();
                }
            });
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void connectionLost(Throwable cause) {
    }

    @Override
    public void messageArrived(String topic, MqttMessage message) throws Exception {
        /*
        * To test ,publish  "open"/"close" at topic you subscibed app to in above .
        * */
        ImageView doorImage = (ImageView)findViewById(R.id.door_image);
        Log.d("door",message.toString());
        if(message.toString().equals("close")){
            doorImage.setImageResource(R.drawable.closed_door);
        }
        else {
            doorImage.setImageResource(R.drawable.open_door);
        }
        Toast.makeText(MainActivity.this, "Topic: "+topic+"\nMessage: "+message, Toast.LENGTH_LONG).show();
        process();
    }

    @Override
    public void deliveryComplete(IMqttDeliveryToken token) {
    }
    /*************************************************************************************/

    /**********************************Camera***************************************************/

    private File imageFile;

    public void process(){
        Intent intent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
        imageFile = new File(Environment.getExternalStoragePublicDirectory( Environment.DIRECTORY_DCIM ), "test.jpg");

        Uri tempuri = Uri.fromFile(imageFile);
        intent.putExtra(MediaStore.EXTRA_OUTPUT, tempuri);
        intent.putExtra(MediaStore.EXTRA_VIDEO_QUALITY, 1);
        startActivityForResult( intent, 0 );
    }

    protected void onActivityResult(int requestCode, int resultCode, Intent data){
        if (requestCode == 0){
            switch(resultCode){
                case Activity.RESULT_OK:
                    if (imageFile.exists()){
                        Toast.makeText(this, "The file was saved at " + imageFile.getAbsolutePath(), Toast.LENGTH_LONG).show();
                    }
                    else{
                        Toast.makeText(this, ".....", Toast.LENGTH_LONG).show();
                    }
                    break;
                case Activity.RESULT_CANCELED:
                    break;
                default:
                    break;
            }
        }
    }

    /*************************************************************************************/

}
