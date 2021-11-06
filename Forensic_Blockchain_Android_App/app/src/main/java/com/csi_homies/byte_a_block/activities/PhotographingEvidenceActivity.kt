package com.csi_homies.byte_a_block.activities

import android.app.Activity
import android.app.AlertDialog
import android.content.ActivityNotFoundException
import android.content.Intent
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.os.Environment
import android.provider.MediaStore
import android.view.Menu
import android.view.MenuItem
import android.widget.Toast
import androidx.core.content.FileProvider
import com.csi_homies.byte_a_block.utils.Constants
import kotlinx.android.synthetic.main.activity_photographing_evidence.*
import java.io.File
import com.csi_homies.byte_a_block.utils.GetProperImageRotation


private const val REQUEST_CODE = 42
private const val FILE_NAME = "photo.jpg"

private lateinit var photoFile: File
private lateinit var rotatedImageFile: File
private lateinit var takenImageBitmap:Bitmap

class PhotographingEvidenceActivity : AppCompatActivity() {

    // Used for making the button for proceeding to next activity only be present after a photo was taken
    private var confirmPhotoTakenMenu: Menu? = null

    private var getPurposeForThisActivity: Int? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_photographing_evidence)

        getPurposeForThisActivity = intent.getIntExtra(Constants.START_PHOTO_TAKING_ACTIVITY_ID, 0)

        if (getPurposeForThisActivity == Constants.ADD_NEW_EVIDENCE)
            setUpUIAddEvidence(intent.getStringExtra(Constants.SELECTED_CASE_NAME_ID))
         else if (getPurposeForThisActivity == Constants.MODIFY_EVIDENCE_STATUS)
            setUpUIModifyEvidenceStatus(intent.getIntExtra(Constants.SELECTED_EVIDENCE_ID_ID, 0).toString())

        addEvidenceImageButton.setOnClickListener {

            val takePictureIntent = Intent(MediaStore.ACTION_IMAGE_CAPTURE)
            photoFile = FILE_NAME.getPhotoFile()

            val fileProvider = FileProvider.getUriForFile(this, "com.csi_homies.byte_a_block.fileprovider", photoFile)
            takePictureIntent.putExtra(MediaStore.EXTRA_OUTPUT, fileProvider)
            try {
                startActivityForResult(takePictureIntent, REQUEST_CODE)
            } catch (e: ActivityNotFoundException) {
                Toast.makeText(this, "No camera module found!", Toast.LENGTH_LONG).show()
            }
        }
    }

    private fun String.getPhotoFile(): File {
        val storageDirectory = getExternalFilesDir(Environment.DIRECTORY_PICTURES)
        return File.createTempFile(this, ".jpg", storageDirectory)
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        // If both of the following are true, then the user has successfully taken a picture from the camera
        if (requestCode == REQUEST_CODE && resultCode == Activity.RESULT_OK) {
            rotatedImageFile = GetProperImageRotation.getRotatedImageFile(photoFile, this@PhotographingEvidenceActivity)!!
            takenImageBitmap = BitmapFactory.decodeFile(rotatedImageFile.absolutePath)
            addEvidenceImageView.setImageBitmap(takenImageBitmap)
            confirmPhotoTakenMenu?.findItem(R.id.confirmPhotoButton)?.isVisible = true
        } else {
            super.onActivityResult(requestCode, resultCode, data)
        }
    }

    private fun setUpUIModifyEvidenceStatus(evidenceId: String?) {
        setupActionBar("Updating status for Evidence $evidenceId")
    }

    private fun setUpUIAddEvidence(caseName: String?) {
        setupActionBar("New Evidence for Case ${caseName.toString()}")
    }

    private fun setupActionBar(actionBarTitle: String) {
        var actionBar = supportActionBar
        if (actionBar != null) {
            actionBar.title = actionBarTitle
            actionBar.setHomeAsUpIndicator(R.drawable.outline_clear_black_36)
            actionBar.setDisplayHomeAsUpEnabled(true)
        }
    }

    override fun onSupportNavigateUp(): Boolean {
        onBackPressed()
        finish()
        return super.onSupportNavigateUp()
    }

    override fun onCreateOptionsMenu(menu: Menu?): Boolean {
        menuInflater.inflate(R.menu.confirm_photo_taken_menu, menu)
        confirmPhotoTakenMenu = menu
        confirmPhotoTakenMenu?.findItem(R.id.confirmPhotoButton)?.isVisible = false
        return super.onCreateOptionsMenu(menu)
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        when (item.itemId){
            R.id.confirmPhotoButton -> {
                val builder = AlertDialog.Builder(this@PhotographingEvidenceActivity)
                builder.setMessage("Confirm Photo?")
                    .setCancelable(false)
                    .setPositiveButton("Yes") {
                            _, _ ->
                        if (item.itemId == R.id.confirmPhotoButton) {
                            if (getPurposeForThisActivity == Constants.ADD_NEW_EVIDENCE) {
                                // Go to AddEvidenceActivity if the intent of opening this activity is to add new evidence
                                val i = Intent(this@PhotographingEvidenceActivity, AddEvidenceActivity::class.java)
                                i.putExtra(Constants.IMAGE_FILEPATH_ID, rotatedImageFile.absolutePath)
                                i.putExtra(Constants.SELECTED_CASE_NAME_ID, intent.getStringExtra(Constants.SELECTED_CASE_NAME_ID))
                                i.putExtra(Constants.SELECTED_CASE_ID_ID, intent.getIntExtra(Constants.SELECTED_CASE_ID_ID, 0))
                                startActivity(i)
                                finish()
                            }
                            else if (getPurposeForThisActivity == Constants.MODIFY_EVIDENCE_STATUS){
                                val i = Intent(this@PhotographingEvidenceActivity, ModifyEvidenceActivity::class.java)
                                i.putExtra(Constants.IMAGE_FILEPATH_ID, rotatedImageFile.absolutePath)
                                i.putExtra(Constants.SELECTED_CASE_ID_ID, intent.getIntExtra(Constants.SELECTED_CASE_ID_ID, 0))
                                i.putExtra(Constants.SELECTED_EVIDENCE_ID_ID, intent.getIntExtra(Constants.SELECTED_EVIDENCE_ID_ID, 0))
                                startActivity(i)
                                finish()
                            }
                        }
                    }
                    .setNegativeButton("No") {
                            _, _ ->
                    }
                    .show()
            }
        }
        return super.onOptionsItemSelected(item)
    }
}