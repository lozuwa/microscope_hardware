package pfmmedical.clickcamera;

import java.util.ArrayList;
import java.util.List;

import android.Manifest;
import android.app.AlertDialog;
import android.app.ProgressDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.database.Cursor;
import android.net.Uri;
import android.os.Environment;
import android.provider.MediaStore;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.Spinner;
import android.widget.Toast;

import com.squareup.picasso.Picasso;

import java.io.File;

import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.RequestBody;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class MainActivity extends AppCompatActivity implements AdapterView.OnItemSelectedListener {

    /** Global variables */
    private static final String[] PERMISSIONS_READ_STORAGE = new String[]{Manifest.permission.READ_EXTERNAL_STORAGE};
    PermissionsChecker checker;
    public Context mContext;
    public ImageView imageView;
    public String imagePath = "";
    public File imageFile;
    public Spinner spinner;
    public String item;

    final boolean checked_state[]={false,false,false}; //The array that holds the checked state of the checkbox items
    final CharSequence[] colors_radio={"Green","Black","White"}; //items in the alertdialog that displays radiobuttons
    Button list,check,radio;

    /** Constructor */
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        mContext = getApplicationContext();
        imageView = (ImageView) findViewById(R.id.imageView);
        checker = new PermissionsChecker(this);

        /*******************************SPINNER**********************************************/
        spinner = (Spinner) findViewById(R.id.parasite_spinner);
        spinner.setOnItemSelectedListener(this);
        List<String> list = new ArrayList<String>();
        list.add("Nada selecionado");
        list.add("Entamoeba coli");
        list.add("Entamoeba histolica");
        list.add("Trozofoito");
        list.add("Giaria lamblia");
        list.add("Idomoeba butschili");
        ArrayAdapter<String> adp = new ArrayAdapter<String>(this, android.R.layout.simple_dropdown_item_1line, list);
        ArrayAdapter<CharSequence> adapter = ArrayAdapter.createFromResource(this,
                R.array.parasite_array, android.R.layout.select_dialog_singlechoice);
        adp.setDropDownViewResource((android.R.layout.simple_list_item_1));
        spinner.setAdapter(adp);
        /***********************************************************************************/

        AlertDialog.Builder builder2 = new AlertDialog.Builder(MainActivity.this).setTitle("Choose an option")
                .setSingleChoiceItems(colors_radio, -1, new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which){
                        // TODO Auto-generated method stub
                        Toast.makeText(getApplicationContext(),"The selected color is "+colors_radio[which], Toast.LENGTH_LONG).show();
                        dialog.dismiss();
                    }
                });
        AlertDialog alertdialog2 = builder2.create();

        /**Floating buttons*/
        FloatingActionButton fab = (FloatingActionButton) findViewById(R.id.fab);
        assert fab != null;
        fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (InternetConnection.checkConnection(mContext) && !imagePath.isEmpty()) {
                    uploadImage();}
                else {
                    Toast.makeText(MainActivity.this, "Toma una foto", Toast.LENGTH_SHORT).show();}
            }
        });

        FloatingActionButton cam  = (FloatingActionButton) findViewById(R.id.cam);
        assert cam != null;
        cam.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View view){
                StartCamera();
            }
        });

        FloatingActionButton gal = (FloatingActionButton) findViewById(R.id.gal);
        assert gal != null;
        gal.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View view){
                PickGallery();
            }
        });
    }

    /** Pick image from gallery*/
    public void PickGallery(){
        if (checker.lacksPermissions(PERMISSIONS_READ_STORAGE)) {
            startPermissionsActivity(PERMISSIONS_READ_STORAGE);
        }
        else {
            final Intent galleryIntent = new Intent();
            galleryIntent.setType("image/*");
            galleryIntent.setAction(Intent.ACTION_PICK);
            final Intent chooserIntent = Intent.createChooser(galleryIntent, getString(R.string.string_choose_image));
            startActivityForResult(chooserIntent, 2);
        }
    }

    /** Start camera*/
    public void StartCamera() {
        if (checker.lacksPermissions(PERMISSIONS_READ_STORAGE)) {
            startPermissionsActivity(PERMISSIONS_READ_STORAGE);
        }
        else {
            Intent intent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
            imageFile = new File(Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DCIM), "test.png");
            Uri tempuri = Uri.fromFile(imageFile);
            intent.putExtra(MediaStore.EXTRA_OUTPUT, tempuri);
            intent.putExtra(MediaStore.EXTRA_VIDEO_QUALITY, 1);
            startActivityForResult(intent, 1);
        }
    }

    /** On Result of Image Picked */
    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        if (resultCode == RESULT_OK && requestCode == 1) {
            if ( imageFile.exists() ) {
                imagePath = imageFile.getAbsolutePath();
                Picasso.with(mContext).load(new File(imagePath)).into(imageView);
                Toast.makeText(MainActivity.this, "The file was saved at " + item + "_" + imageFile.getAbsolutePath(), Toast.LENGTH_SHORT).show();
            }
            else {
                Toast.makeText(MainActivity.this, "There was a problem taking the picture", Toast.LENGTH_SHORT).show();}
        }
        else if (resultCode == RESULT_OK && requestCode == 2){
            super.onActivityResult(requestCode, resultCode, data);
            if (data == null) {
                return;
            }
            Uri selectedImageUri = data.getData();
            String[] filePathColumn = {MediaStore.Images.Media.DATA};
            Cursor cursor = getContentResolver().query(selectedImageUri, filePathColumn, null, null, null);
            if (cursor != null) {
                cursor.moveToFirst();
                int columnIndex = cursor.getColumnIndex(filePathColumn[0]);
                imagePath = cursor.getString(columnIndex);
                Picasso.with(mContext).load(new File(imagePath)).into(imageView);
                Toast.makeText(MainActivity.this, R.string.string_reselect, Toast.LENGTH_LONG).show();
                cursor.close();
            }
            else {
                Toast.makeText(MainActivity.this, R.string.string_unable_to_load_image, Toast.LENGTH_LONG).show();
            }
        }
        else{
        }
    }

    /**Upload Image Client Code*/
    private void uploadImage() {
        /**Progressbar to Display if you need*/
        final ProgressDialog progressDialog;
        progressDialog = new ProgressDialog(MainActivity.this);
        progressDialog.setMessage(getString(R.string.string_title_upload_progressbar_));
        progressDialog.show();

        //Create Upload Server Client
        ApiService service = RetroClient.getApiService();

        //File creating from selected URL
        File file = new File(imagePath);

        // create RequestBody instance from file
        RequestBody requestFile = RequestBody.create(MediaType.parse("multipart/form-data"), file);

        // MultipartBody.Part is used to send also the actual file name
        MultipartBody.Part body = MultipartBody.Part.createFormData("file", item + "_" + file.getName(), requestFile);

        Call<Result> resultCall = service.uploadImage(body);

        // finally, execute the request
        resultCall.enqueue(new Callback<Result>() {
            @Override
            public void onResponse(Call<Result> call, Response<Result> response) {
                imagePath = "";
                Toast.makeText(MainActivity.this, response.toString(), Toast.LENGTH_SHORT).show();
                Toast.makeText(MainActivity.this, "Success", Toast.LENGTH_SHORT).show();
                progressDialog.dismiss();
            }

            @Override
            public void onFailure(Call<Result> call, Throwable t) {
                imagePath = "";
                Toast.makeText(MainActivity.this, t.toString(), Toast.LENGTH_LONG).show();
                progressDialog.dismiss();
            }
        });
    }

    @Override
    public void onItemSelected(AdapterView<?> adapterView, View view, int position, long l) {
        String item_ = adapterView.getItemAtPosition(position).toString();
        if (item_.split(" ").length > 1) {
            item = item_.split(" ")[0] + "_" + item_.split(" ")[1];
        }
        else {
            item = item_;
        }
        Toast.makeText(MainActivity.this, item, Toast.LENGTH_SHORT).show();
    }

    @Override
    public void onNothingSelected(AdapterView<?> adapterView) {
    }

    private void startPermissionsActivity(String[] permission) {
        PermissionsActivity.startActivityForResult(this, 0, permission);
    }
}
